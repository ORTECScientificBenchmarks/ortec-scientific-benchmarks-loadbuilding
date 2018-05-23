import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDboxkind   import ThreeDboxkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace import ThreeDloadingspace

class TestBoxkind(unittest.TestCase):
    def setUp(self):
        self.box_kind = ThreeDboxkind()
        self.box_kind.id = 1
        self.box_kind.quantity = 1
        self.box_kind.boundingBox = [750, 750, 10]
        self.box_kind.position = [0, 0, 0]
        self.box_kind.loadingspace = ThreeDloadingspace()
        self.box_kind.loadingspace.id = 1
        self.box_kind.loadingspace.boundingBox = [750, 750, 1500]
        self.box_kind.loadingspace.position = [0, 0, 10]
        self.box_kind.orientations = set(['LWH', 'WLH'])
        
    def test_boxkind_valid(self):
        self.assertTrue(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_id1(self):
        self.box_kind.id = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_id2(self):
        self.box_kind.id = "1"
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_boundingbox1(self):
        self.box_kind.boundingBox = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_boundingbox2(self):
        self.box_kind.boundingBox = "0,0,0"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_boundingbox3(self):
        self.box_kind.boundingBox[0] = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_boundingbox4(self):
        self.box_kind.boundingBox[0] = "a"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_boundingbox5(self):
        self.box_kind.boundingBox[0] = -1
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_position1(self):
        self.box_kind.position = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_position2(self):
        self.box_kind.position = "0,0,0"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_position3(self):
        self.box_kind.position[0] = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_position4(self):
        self.box_kind.position[0] = "a"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_position5(self):
        self.box_kind.position[0] = -1
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_loadingspace1(self):
        self.box_kind.loadingspace = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_loadingspace2(self):
        self.box_kind.loadingspace = object()
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_loadingspace3(self):
        self.box_kind.loadingspace = ThreeDloadingspace()
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_quantity1(self):
        self.box_kind.quantity = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_quantity2(self):
        self.box_kind.quantity = "1"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_quantity3(self):
        self.box_kind.quantity = -1
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_invalid_orientations1(self):
        self.box_kind.orientations = None
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_orientations2(self):
        self.box_kind.orientations = "LWH,WLH"
        self.assertFalse(self.box_kind.IsValid()[0])
    def test_boxkind_invalid_orientations3(self):
        self.box_kind.orientations = set(["LLL"])
        self.assertFalse(self.box_kind.IsValid()[0])

    def test_boxkind_typestring(self):
        self.assertEqual(self.box_kind.TypeString(), "boxkind")
        
    def test_boxkind_ne(self):
        self.assertNotEqual(self.box_kind, ThreeDboxkind())
    
TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoxkind))