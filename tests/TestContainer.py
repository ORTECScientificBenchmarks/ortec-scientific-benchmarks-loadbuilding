import unittest
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDcontainer import ThreeDcontainer
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDloadingspace  import ThreeDloadingspace

class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = ThreeDcontainer()
        self.container.id = 1
        self.container.kindid = 1
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.placements = []
        self.container.addLoadingspace(loadingspace)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 2
        loadingspace.placements = []
        self.container.addLoadingspace(loadingspace)
        
    def test_container_valid(self):
        self.assertTrue(self.container.IsValid()[0])

    def test_container_invalid_id1(self):
        self.container.id = None
        self.assertFalse(self.container.IsValid()[0])
    def test_container_invalid_id2(self):
        self.container.id = "1"
        self.assertFalse(self.container.IsValid()[0])

    def test_container_invalid_kindid1(self):
        self.container.kindid = None
        self.assertFalse(self.container.IsValid()[0])
    def test_container_invalid_kindid2(self):
        self.container.kindid = "1"
        self.assertFalse(self.container.IsValid()[0])

    def test_container_invalid_loadingspace(self):
        self.container.loadingspaces[0] = None
        self.assertFalse(self.container.IsValid()[0])
    def test_container_duplicate_loadingspace_ids(self):
        self.container.loadingspaces[0].id = 2
        self.assertFalse(self.container.IsValid()[0])
    
    def test_container_typestring(self):
        self.assertEqual(self.container.TypeString(), "container")
        
    def test_container_ne(self):
        self.assertNotEqual(self.container, ThreeDcontainer())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestContainer))