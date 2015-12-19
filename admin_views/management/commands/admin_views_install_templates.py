from __future__ import print_function
import django
import os
from shutil import copyfile

from distutils.version import StrictVersion
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Install the changed admin index template """

    can_import_settings = True
    args = "/path/to/install/template"
    help = "Install the necessary changed admin template by providing it as an argument or at the prompt"

    def handle(self, *args, **options):
        current_dir = os.path.dirname(__file__)
        if StrictVersion(django.get_version()) < StrictVersion('1.8'):
            template_dirs = settings.TEMPLATE_DIRS
        else:
            template_dirs = []
            for template_engine in settings.TEMPLATES:
                if template_engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
                    template_dirs = template_dirs + template_engine['DIRS']

        if args:
            # Handle case where dir specified on commandline
            dest_dir = os.path.join(args[0], 'admin/')
        elif len(template_dirs) == 1:
            # Handle common case where only one template directory is defined
            dest_dir = os.path.join(template_dirs[0], 'admin/')
        else:
            # Give user the option of picking which directory from their list
            print("Which directory would you like the templates installed in?")
            print("NOTE: The first is *usually* the correct answer.")
            print()

            for i, dir in enumerate(template_dirs, start=1):
                print("    %d) %s" % (i, dir))

            print()

            try:
               input = raw_input
            except NameError:
               pass

            input_ = input('Enter directory number: ')
            try:
                dir_num = int(input_)
            except ValueError:
                print("ERROR: %r is not a number, please try again." % input_)
                return

            dest_dir = os.path.join(template_dirs[dir_num-1], 'admin/')

        print("Copying templates to '%s'" % dest_dir)

        # Create the admin directory if necessary
        if not os.path.exists(dest_dir):
            print("Creating intermediate directories...")
            os.makedirs(dest_dir)

        copyfile(
                os.path.join(current_dir, "../../templates/admin/index.html"),
                os.path.join(dest_dir, "index.html")
            )

        print("Done.")
