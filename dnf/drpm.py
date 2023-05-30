# drpm.py
# Delta RPM support
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
from binascii import hexlify
from dnf.yum.misc import unlink_f
from dnf.i18n import _

import dnf.callback
import dnf.logging
import dnf.repo
import hawkey
import logging
import libdnf.repo
import os

APPLYDELTA = '/usr/bin/applydeltarpm'

logger = logging.getLogger("dnf")


class DeltaPayload(dnf.repo.PackagePayload):
    def __init__(self, delta_info, delta, pkg, progress):
        super(DeltaPayload, self).__init__(pkg, progress)
        self.delta_info = delta_info
        self.delta = delta

    def __str__(self):
        return os.path.basename(self.delta.location)

    def _end_cb(self, cbdata, lr_status, msg):
        super(DeltaPayload, self)._end_cb(cbdata, lr_status, msg)
        if lr_status != libdnf.repo.PackageTargetCB.TransferStatus_ERROR:
            self.delta_info.enqueue(self)

    def _target_params(self):
        delta = self.delta
        ctype, csum = delta.chksum
        ctype = hawkey.chksum_name(ctype)
        chksum = hexlify(csum).decode()

        ctype_code = libdnf.repo.PackageTarget.checksumType(ctype)
        if ctype_code == libdnf.repo.PackageTarget.ChecksumType_UNKNOWN:
            logger.warning(_("unsupported checksum type: %s"), ctype)

        return {
            'relative_url' : delta.location,
            'checksum_type' : ctype_code,
            'checksum' : chksum,
            'expectedsize' : delta.downloadsize,
            'base_url' : delta.baseurl,
        }

    @property
    def download_size(self):
        return self.delta.downloadsize

    @property
    def _full_size(self):
        return self.pkg.downloadsize

    def localPkg(self):
        location = self.delta.location
        return os.path.join(self.pkg.repo.pkgdir, os.path.basename(location))


class DeltaInfo(object):
    def __init__(self, query, progress, deltarpm_percentage=None):
        '''A delta lookup and rebuild context
           query -- installed packages to use when looking up deltas
           progress -- progress obj to display finished delta rebuilds
        '''
        self.deltarpm_installed = False
        if os.access(APPLYDELTA, os.X_OK):
            self.deltarpm_installed = True
        try:
            self.deltarpm_jobs = os.sysconf('SC_NPROCESSORS_ONLN')
        except (TypeError, ValueError):
            self.deltarpm_jobs = 4
        if deltarpm_percentage is None:
            self.deltarpm_percentage = dnf.conf.Conf().deltarpm_percentage
        else:
            self.deltarpm_percentage = deltarpm_percentage
        self.query = query
        self.progress = progress

        self.queue = []
        self.jobs = {}
        self.err = {}

    def delta_factory(self, po, progress):
        '''Turn a po to Delta RPM po, if possible'''
        if not self.deltarpm_installed:
            # deltarpm is not installed
            return None
        if not po.repo.deltarpm or not self.deltarpm_percentage:
            # drpm disabled
            return None
        if po._is_local_pkg():
            # drpm disabled for local
            return None
        if os.path.exists(po.localPkg()):
            # already there
            return None

        best = po._size * self.deltarpm_percentage / 100
        best_delta = None
        for ipo in self.query.filter(name=po.name, arch=po.arch):
            delta = po.get_delta_from_evr(ipo.evr)
            if delta and delta.downloadsize < best:
                best = delta.downloadsize
                best_delta = delta
        if best_delta:
            return DeltaPayload(self, best_delta, po, progress)
        return None

    def job_done(self, pid, code):
        # handle a finished delta rebuild
        logger.log(dnf.logging.SUBDEBUG, 'drpm: %d: return code: %d, %d', pid,
                   code >> 8, code & 0xff)

        pload = self.jobs.pop(pid)
        pkg = pload.pkg
        if code != 0:
            unlink_f(pload.pkg.localPkg())
            self.err[pkg] = [_('Delta RPM rebuild failed')]
        elif not pload.pkg.verifyLocalPkg():
            self.err[pkg] = [_('Checksum of the delta-rebuilt RPM failed')]
        else:
            os.unlink(pload.localPkg())
            self.progress.end(pload, dnf.callback.STATUS_DRPM, _('done'))

    def start_job(self, pload):
        # spawn a delta rebuild job
        spawn_args = [APPLYDELTA, APPLYDELTA,
                      '-a', pload.pkg.arch,
                      pload.localPkg(), pload.pkg.localPkg()]
        pid = os.spawnl(os.P_NOWAIT, *spawn_args)
        logger.log(dnf.logging.SUBDEBUG, 'drpm: spawned %d: %s', pid,
                   ' '.join(spawn_args[1:]))
        self.jobs[pid] = pload

    def enqueue(self, pload):
        # process finished jobs, start new ones
        while self.jobs:
            pid, code = os.waitpid(-1, os.WNOHANG)
            if not pid:
                break
            self.job_done(pid, code)
        self.queue.append(pload)
        while len(self.jobs) < self.deltarpm_jobs:
            self.start_job(self.queue.pop(0))
            if not self.queue:
                break

    def wait(self):
        '''Wait until all jobs have finished'''
        while self.jobs:
            pid, code = os.wait()
            self.job_done(pid, code)
            if self.queue:
                self.start_job(self.queue.pop(0))
