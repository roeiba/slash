"""
Test the usage of FQDNs in Slash, to uniquely identify tests being run.
"""
import os
import shutil
import tempfile

import slash
from .utils import TestCase
from .utils import run_tests_assert_success

class FQDNTestBase(TestCase):

    def setUp(self):
        super(FQDNTestBase, self).setUp()
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        self.filename = os.path.join(self.root, "testfile.py")
        with open(self.filename, "w") as f:
            f.write(_TEST_TEMPLATE)

        self.session = run_tests_assert_success(slash.loader.Loader().iter_path(self.filename))
        self.results = list(self.session.result.iter_test_results())

class FQDNTest(FQDNTestBase):

    def test_fqdn(self):
        simple_test_fqdn = self.results[0].test_metadata.fqdn
        self.assertEquals(str(simple_test_fqdn), "{0}:TestClass.test_method".format(self.filename))

class FQDNFromPycFilesTest(FQDNTestBase):

    def setUp(self):
        super(FQDNFromPycFilesTest, self).setUp()
        self.new_filename = self.filename + "c"
        assert self.new_filename.endswith(".pyc")
        self.fqdn = self.results[0].test_metadata.fqdn

    def test_pyc_files_original_exists(self):
        "Filenames ending with .pyc should be normalized to .py"
        self.fqdn.set_path(self.new_filename)
        self.assertEquals(self.fqdn.get_path(), self.filename)

    def test_pyc_files_original_missing(self):
        "When the original python file is missing and the filename ends with .pyc, it should not be fixed"
        os.unlink(self.filename)
        self.fqdn.set_path(self.new_filename)
        self.assertEquals(self.fqdn.get_path(), self.new_filename)


_TEST_TEMPLATE = """
import slash

class TestClass(slash.Test):
    def test_method(self):
        pass

    @slash.parameters.iterate(x=[1, 2, 3])
    def test_parameters(self, x):
       pass
"""
