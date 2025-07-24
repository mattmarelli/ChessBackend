from django.test.runner import DiscoverRunner
from phytochrome.settings import DATABASES

databases = frozenset(DATABASES.keys())


class BackendTestRunner(DiscoverRunner):
    def run_checks(self, databases):
        # call_command("import_data", "--update", "--verbosity", "0")
        # call_command("import_data_individual_files")
        return super().run_checks(databases)
