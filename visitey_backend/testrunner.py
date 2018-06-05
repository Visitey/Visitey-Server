from django.conf import settings
from django_nose import NoseTestSuiteRunner


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


class Runner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None):
        settings.MIGRATION_MODULES = DisableMigrations()
        super(Runner, self).run_tests(test_labels, extra_tests=extra_tests)