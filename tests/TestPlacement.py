import unittest
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDplacement import ThreeDplacement

class TestPlacement(unittest.TestCase):
    def setUp(self):
        self.itemplacement = ThreeDplacement()
        self.itemplacement.id = 1
        self.itemplacement.itemid = 1
        self.itemplacement.position = [0, 0, 0]
        self.itemplacement.orientation = "LWH"
        self.boxplacement = ThreeDplacement()
        self.boxplacement.id = 2
        self.boxplacement.boxid = 1
        self.boxplacement.position = [0, 0, 0]
        self.boxplacement.orientation = "LWH"
        self.palletplacement = ThreeDplacement()
        self.palletplacement.id = 3
        self.palletplacement.boxid = 1
        self.palletplacement.position = [0, 0, 0]
        self.palletplacement.orientation = "LWH"
        
    def test_placement_valid(self):
        self.assertTrue(self.itemplacement.IsValid()[0])

    def test_placement_invalid_id1(self):
        self.itemplacement.id = None
        self.assertFalse(self.itemplacement.IsValid()[0])
    def test_placement_invalid_id2(self):
        self.itemplacement.id = "1"
        self.assertFalse(self.itemplacement.IsValid()[0])

    def test_placement_multiple_id_types(self):
        self.itemplacement.boxid = 1
        self.assertFalse(self.itemplacement.IsValid()[0])
        self.boxplacement.palletid = 1
        self.assertFalse(self.boxplacement.IsValid()[0])
        self.palletplacement.itemid = 1
        self.assertFalse(self.palletplacement.IsValid()[0])
        self.itemplacement.palletid = 1
        self.assertFalse(self.itemplacement.IsValid()[0])

    def test_placement_invalid_itemid1(self):
        self.itemplacement.itemid = None
        self.assertFalse(self.itemplacement.IsValid()[0])
    def test_placement_invalid_itemid2(self):
        self.itemplacement.itemid = "1"
        self.assertFalse(self.itemplacement.IsValid()[0])
    
    def test_placement_invalid_boxid1(self):
        self.boxplacement.boxid = None
        self.assertFalse(self.boxplacement.IsValid()[0])
    def test_placement_invalid_boxid2(self):
        self.boxplacement.boxid = "1"
        self.assertFalse(self.boxplacement.IsValid()[0])

    def test_placement_invalid_palletid1(self):
        self.palletplacement.boxid = None
        self.assertFalse(self.palletplacement.IsValid()[0])
    def test_placement_invalid_palletid2(self):
        self.palletplacement.boxid = "1"
        self.assertFalse(self.palletplacement.IsValid()[0])

    def test_placement_typestring(self):
        self.assertEqual(self.itemplacement.TypeString(), "placement")
        
    def test_placement_ne(self):
        self.assertNotEqual(self.itemplacement, ThreeDplacement())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPlacement))