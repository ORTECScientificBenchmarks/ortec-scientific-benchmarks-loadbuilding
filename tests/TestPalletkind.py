import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDpalletkind   import ThreeDpalletkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace import ThreeDloadingspace

class TestPalletkind(unittest.TestCase):
    def setUp(self):
        self.pallet_kind = ThreeDpalletkind()
        self.pallet_kind.id = 1
        self.pallet_kind.quantity = 1
        self.pallet_kind.boundingBox = [750, 750, 10]
        self.pallet_kind.position = [0, 0, 0]
        self.pallet_kind.loadingspace = ThreeDloadingspace()
        self.pallet_kind.loadingspace.id = 1
        self.pallet_kind.loadingspace.boundingBox = [750, 750, 1500]
        self.pallet_kind.loadingspace.position = [0, 0, 10]
        self.pallet_kind.orientations = set(['LWH', 'WLH'])
        
    def test_palletkind_valid(self):
        self.assertTrue(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_id1(self):
        self.pallet_kind.id = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_id2(self):
        self.pallet_kind.id = "1"
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_boundingbox1(self):
        self.pallet_kind.boundingBox = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_boundingbox2(self):
        self.pallet_kind.boundingBox = "0,0,0"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_boundingbox3(self):
        self.pallet_kind.boundingBox[0] = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_boundingbox4(self):
        self.pallet_kind.boundingBox[0] = "a"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_boundingbox5(self):
        self.pallet_kind.boundingBox[0] = -1
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_position1(self):
        self.pallet_kind.position = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_position2(self):
        self.pallet_kind.position = "0,0,0"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_position3(self):
        self.pallet_kind.position[0] = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_position4(self):
        self.pallet_kind.position[0] = "a"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_position5(self):
        self.pallet_kind.position[0] = -1
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_loadingspace1(self):
        self.pallet_kind.loadingspace = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_loadingspace2(self):
        self.pallet_kind.loadingspace = object()
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_loadingspace3(self):
        self.pallet_kind.loadingspace = ThreeDloadingspace()
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_quantity1(self):
        self.pallet_kind.quantity = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_quantity2(self):
        self.pallet_kind.quantity = "1"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_quantity3(self):
        self.pallet_kind.quantity = -1
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_invalid_orientations1(self):
        self.pallet_kind.orientations = None
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_orientations2(self):
        self.pallet_kind.orientations = "LWH,WLH"
        self.assertFalse(self.pallet_kind.IsValid()[0])
    def test_palletkind_invalid_orientations3(self):
        self.pallet_kind.orientations = set(["LLL"])
        self.assertFalse(self.pallet_kind.IsValid()[0])

    def test_palletkind_typestring(self):
        self.assertEqual(self.pallet_kind.TypeString(), "palletkind")
        
    def test_palletkind_ne(self):
        self.assertNotEqual(self.pallet_kind, ThreeDpalletkind())
    
TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPalletkind))