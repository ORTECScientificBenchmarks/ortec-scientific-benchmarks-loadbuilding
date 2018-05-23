import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDcontainerkind import ThreeDcontainerkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace  import ThreeDloadingspace
    
class TestContainerkind(unittest.TestCase):
    def setUp(self):
        self.container_kind = ThreeDcontainerkind()
        self.container_kind.id = 1
        self.container_kind.quantity = 1
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [0, 0, 0]
        self.container_kind.addLoadingspace(loadingspace)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 2
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [2000, 0, 0]
        self.container_kind.addLoadingspace(loadingspace)
        
    def test_containerkind_valid(self):
        self.assertTrue(self.container_kind.IsValid()[0])

    def test_containerkind_invalid_id1(self):
        self.container_kind.id = None
        self.assertFalse(self.container_kind.IsValid()[0])
    def test_containerkind_invalid_id2(self):
        self.container_kind.id = "1"
        self.assertFalse(self.container_kind.IsValid()[0])

    def test_containerkind_invalid_loadingspace(self):
        self.container_kind.loadingspaces[0] = None
        self.assertFalse(self.container_kind.IsValid()[0])
    def test_containerkind_duplicate_loadingspace_ids(self):
        self.container_kind.loadingspaces[0].id = 2
        self.assertFalse(self.container_kind.IsValid()[0])

    def test_containerkind_invalid_quantity1(self):
        self.container_kind.quantity = None
        self.assertFalse(self.container_kind.IsValid()[0])
    def test_containerkind_invalid_quantity2(self):
        self.container_kind.quantity = "1"
        self.assertFalse(self.container_kind.IsValid()[0])
    def test_containerkind_invalid_quantity3(self):
        self.container_kind.quantity = -1
        self.assertFalse(self.container_kind.IsValid()[0])
    
    def test_containerkind_typestring(self):
        self.assertEqual(self.container_kind.TypeString(), "containerkind")
        
    def test_containerkind_ne(self):
        self.assertNotEqual(self.container_kind, ThreeDcontainerkind())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestContainerkind))