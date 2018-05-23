import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDdescription   import ThreeDdescription

class TestDescription(unittest.TestCase):
    def setUp(self):
        self.description = ThreeDdescription()
        self.description.setname = "Description"
        self.description.name    = "Test"

    def test_description_valid(self):
        self.assertTrue(self.description.IsValid()[0])

    def test_description_invalid_setname1(self):
        self.description.setname = None
        self.assertFalse(self.description.IsValid()[0])
    def test_description_invalid_setname2(self):
        self.description.setname = 1
        self.assertFalse(self.description.IsValid()[0])
    def test_description_invalid_setname3(self):
        self.description.setname = ""
        self.assertFalse(self.description.IsValid()[0])

    def test_description_invalid_name1(self):
        self.description.name = None
        self.assertFalse(self.description.IsValid()[0])
    def test_description_invalid_name2(self):
        self.description.name = 1
        self.assertFalse(self.description.IsValid()[0])
    def test_description_invalid_name3(self):
        self.description.name = ""
        self.assertFalse(self.description.IsValid()[0])
        
    def test_description_typestring(self):
        self.assertEqual(self.description.TypeString(), "description")
        
    def test_description_ne(self):
        self.assertNotEqual(self.description, ThreeDdescription())
        
TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDescription))