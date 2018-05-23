import unittest
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDbox           import ThreeDbox
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDloadingspace  import ThreeDloadingspace

class TestBox(unittest.TestCase):
    def setUp(self):
        self.box = ThreeDbox()
        self.box.id = 1
        self.box.kindid = 1
        self.box.loadingspace = ThreeDloadingspace()
        self.box.loadingspace.id = 1
        self.box.loadingspace.placements = []
        
    def test_box_valid(self):
        self.assertTrue(self.box.IsValid()[0])

    def test_box_invalid_id1(self):
        self.box.id = None
        self.assertFalse(self.box.IsValid()[0])
    def test_box_invalid_id2(self):
        self.box.id = "1"
        self.assertFalse(self.box.IsValid()[0])

    def test_box_invalid_kindid1(self):
        self.box.kindid = None
        self.assertFalse(self.box.IsValid()[0])
    def test_box_invalid_kindid2(self):
        self.box.kindid = "1"
        self.assertFalse(self.box.IsValid()[0])

    def test_box_invalid_loadingspace(self):
        self.box.loadingspace = None
        self.assertFalse(self.box.IsValid()[0])
    
    def test_box_typestring(self):
        self.assertEqual(self.box.TypeString(), "box")
        
    def test_box_ne(self):
        self.assertNotEqual(self.box, ThreeDbox())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBox))