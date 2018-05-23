import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace  import ThreeDloadingspace

class TestLoadingspace(unittest.TestCase):
    def setUp(self):
        self.test_loadingspace = ThreeDloadingspace()
        self.test_loadingspace.id = 1
        self.test_loadingspace.boundingBox = [2000, 1000, 1000]
        self.test_loadingspace.position = [0, 0, 0]

    def test_loadingspace_valid(self):
        self.assertTrue(self.test_loadingspace.IsValid()[0])
        
    def test_loadingspace_invalid_id1(self):
        self.test_loadingspace.id = None
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_id2(self):
        self.test_loadingspace.id = "1"
        self.assertFalse(self.test_loadingspace.IsValid()[0])

    def test_loadingspace_invalid_boundingbox1(self):
        self.test_loadingspace.boundingBox = None
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_boundingbox2(self):
        self.test_loadingspace.boundingBox = "0,0,0"
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_boundingbox3(self):
        self.test_loadingspace.boundingBox[0] = None
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_boundingbox4(self):
        self.test_loadingspace.boundingBox[0] = "a"
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_boundingbox5(self):
        self.test_loadingspace.boundingBox[0] = -1
        self.assertFalse(self.test_loadingspace.IsValid()[0])

    def test_loadingspace_invalid_position1(self):
        self.test_loadingspace.position = None
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_position2(self):
        self.test_loadingspace.position = "0,0,0"
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_position3(self):
        self.test_loadingspace.position[0] = None
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_position4(self):
        self.test_loadingspace.position[0] = "a"
        self.assertFalse(self.test_loadingspace.IsValid()[0])
    def test_loadingspace_invalid_position5(self):
        self.test_loadingspace.position[0] = -1
        self.assertFalse(self.test_loadingspace.IsValid()[0])

    def test_loadingspace_typestring(self):
        self.assertEqual(self.test_loadingspace.TypeString(), "loadingspace")
        
    def test_loadingspace_ne(self):
        self.assertNotEqual(self.test_loadingspace, ThreeDloadingspace())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLoadingspace))