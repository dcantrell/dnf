# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

"""A plugin that lists installed packages that are obsoleted by any available package"""

from dnf.i18n import _
import dnf
import dnf.cli


# If you only plan to create a new dnf subcommand in a plugin
# you can use @dnf.plugin.register_command decorator instead of creating
# a Plugin class which only registers the command
# (for full-fledged Plugin class see examples/install_plugin.py)
@dnf.plugin.register_command
class Command(dnf.cli.Command):

    """A command that lists packages installed on the system that are
       obsoleted by packages in any known repository."""

    # An alias is needed to invoke the command from command line.
    aliases = ['foo']  # <-- SET YOUR ALIAS HERE.

    @staticmethod
    def set_argparser(parser):
        parser.add_argument("package", nargs='*', metavar=_('PACKAGE'))

    def configure(self):
        """Setup the demands."""
        # Repositories serve as sources of information about packages.
        self.cli.demands.available_repos = True
        # A sack is needed for querying.
        self.cli.demands.sack_activation = True

    def run(self):
        """Run the command."""

        obs_tuples = []
        # A query matches all available packages
        q = self.base.sack.query()

        if not self.opts.package:
            # Narrow down query to match only installed packages
            inst = q.installed()
            # A dictionary containing list of obsoleted packages
            for new in q.filter(obsoletes=inst):
                obs_reldeps = new.obsoletes
                obsoleted = inst.filter(provides=obs_reldeps).run()
                obs_tuples.extend([(new, old) for old in obsoleted])
        else:
            for pkg_spec in self.opts.package:
                # A subject serves for parsing package format from user input
                subj = dnf.subject.Subject(pkg_spec)
                # A query restricted to installed packages matching given subject
                inst = subj.get_best_query(self.base.sack).installed()
                for new in q.filter(obsoletes=inst):
                    obs_reldeps = new.obsoletes
                    obsoleted = inst.filter(provides=obs_reldeps).run()
                    obs_tuples.extend([(new, old) for old in obsoleted])

        if not obs_tuples:
            raise dnf.exceptions.Error('No matching Packages to list')

        for (new, old) in obs_tuples:
            print('%s.%s obsoletes %s.%s' %
                  (new.name, new.arch, old.name, old.arch))


