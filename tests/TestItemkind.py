import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDitemkind import ThreeDitemkind

class TestItemkind(unittest.TestCase):
    def setUp(self):
        self.item_kind = ThreeDitemkind()
        self.item_kind.id = 1
        self.item_kind.quantity = 10
        self.item_kind.boundingBox = [10,10,10]
        self.item_kind.orientations = set(['LWH', 'WLH'])

    def test_itemkind_valid(self):
        self.assertTrue(self.item_kind.IsValid()[0])

    def test_itemkind_orientationstring(self):
        self.assertEqual(self.item_kind.GetOrientationString(), "LWH,WLH")

    def test_itemkind_invalid_id1(self):
        self.item_kind.id = None
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_id2(self):
        self.item_kind.id = "1"
        self.assertFalse(self.item_kind.IsValid()[0])

    def test_itemkind_invalid_boundingbox1(self):
        self.item_kind.boundingBox = None
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_boundingbox2(self):
        self.item_kind.boundingBox = "0,0,0"
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_boundingbox3(self):
        self.item_kind.boundingBox[0] = None
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_boundingbox4(self):
        self.item_kind.boundingBox[0] = "a"
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_boundingbox5(self):
        self.item_kind.boundingBox[0] = -1
        self.assertFalse(self.item_kind.IsValid()[0])

    def test_itemkind_invalid_quantity1(self):
        self.item_kind.quantity = None
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_quantity2(self):
        self.item_kind.quantity = "1"
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_quantity3(self):
        self.item_kind.quantity = -1
        self.assertFalse(self.item_kind.IsValid()[0])
    
    def test_itemkind_invalid_orientations1(self):
        self.item_kind.orientations = None
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_orientations2(self):
        self.item_kind.orientations = "LWH,HLW"
        self.assertFalse(self.item_kind.IsValid()[0])
    def test_itemkind_invalid_orientations3(self):
        self.item_kind.orientations = set(["LLL"])
        self.assertFalse(self.item_kind.IsValid()[0])
    
    def test_itemkind_typestring(self):
        self.assertEqual(self.item_kind.TypeString(), "itemkind")
        
    def test_itemkind_ne(self):
        self.assertNotEqual(self.item_kind, ThreeDitemkind())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestItemkind))