import unittest
import os

from ortec.scientific.benchmarks.loadbuilding.instance.read.JSONtoThreeDinstance import JSONtoThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.instance.read.XMLtoThreeDinstance  import XMLtoThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.instance.read.YAMLtoThreeDinstance import YAMLtoThreeDinstance

from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDinstance      import ThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDcontainerkind import ThreeDcontainerkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDpalletkind    import ThreeDpalletkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDboxkind       import ThreeDboxkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace  import ThreeDloadingspace
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDitemkind      import ThreeDitemkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDconstraint    import ThreeDconstraint
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDobjective     import ThreeDobjective

def getfilename(name):
    return os.path.join(os.path.dirname(__file__),'..',name)

def loadJSON(filename):
    return JSONtoThreeDinstance(getfilename(filename)).CreateThreeDinstance()

def loadXML(filename): 
    return XMLtoThreeDinstance(getfilename(filename)).CreateThreeDinstance()

def loadYAML(filename):
    return YAMLtoThreeDinstance(getfilename(filename)).CreateThreeDinstance()
    
class TestReadDescription(unittest.TestCase):
    def setUp(self):
        self.test_instance = ThreeDinstance()
        self.test_instance.description.setname = "Description"
        self.test_instance.description.name    = "Test"
        
    def performTest1(self, instance):
        self.assertEqual(instance, self.test_instance)
        self.assertTrue(instance.IsValid()[0])
    def test_description_read_JSON01(self): self.performTest1(loadJSON("tests/read/description/test1.json"))
    def test_description_read_XML01(self):  self.performTest1(loadXML("tests/read/description/test1.xml"))
    def test_description_read_YAML01(self): self.performTest1(loadYAML("tests/read/description/test1.yaml"))

    def performTest2(self, instance):
        self.test_instance.description.setname = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_description_read_JSON02(self): self.performTest2(loadJSON("tests/read/description/test2.json"))
    def test_description_read_XML02(self):  self.performTest2(loadXML("tests/read/description/test2.xml"))
    def test_description_read_YAML02(self): self.performTest2(loadYAML("tests/read/description/test2.yaml"))

class TestReadContainerkind(unittest.TestCase):
    def setUp(self):
        self.test_instance = ThreeDinstance()
        self.test_instance.description.setname = "Containerkind"
        self.test_instance.description.name    = "Test"
        container_kind = ThreeDcontainerkind()
        container_kind.id = 1
        container_kind.quantity = 1
        self.test_instance.addContainerkind(container_kind)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [0, 0, 0]
        container_kind.addLoadingspace(loadingspace)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 2
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [2000, 0, 0]
        container_kind.addLoadingspace(loadingspace)
        container_kind = ThreeDcontainerkind()
        container_kind.id = 2
        container_kind.quantity = 9999
        self.test_instance.addContainerkind(container_kind)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [1000, 500, 500]
        loadingspace.position = [0, 0, 0]
        container_kind.addLoadingspace(loadingspace)

    def performTest1(self, instance):
        self.assertEqual(instance, self.test_instance)
        self.assertTrue(instance.IsValid()[0])
    def test_containerkind_read_JSON01(self): self.performTest1(loadJSON("tests/read/containerkind/test1.json"))
    def test_containerkind_read_XML01(self):  self.performTest1(loadXML("tests/read/containerkind/test1.xml"))
    def test_containerkind_read_YAML01(self): self.performTest1(loadYAML("tests/read/containerkind/test1.yaml"))

    def performTest2(self, instance):
        self.test_instance.containerkinds[0].id = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON02(self): self.performTest2(loadJSON("tests/read/containerkind/test2.json"))
    def test_containerkind_read_XML02(self):  self.performTest2(loadXML("tests/read/containerkind/test2.xml"))
    def test_containerkind_read_YAML02(self): self.performTest2(loadYAML("tests/read/containerkind/test2.yaml"))

    def performTest3(self, instance):
        self.test_instance.containerkinds[0].quantity = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON03(self): self.performTest3(loadJSON("tests/read/containerkind/test3.json"))
    def test_containerkind_read_XML03(self):  self.performTest3(loadXML("tests/read/containerkind/test3.xml"))
    def test_containerkind_read_YAML03(self): self.performTest3(loadYAML("tests/read/containerkind/test3.yaml"))
    
    def performTest4(self, instance):
        self.test_instance.containerkinds[0].loadingspaces = list()
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON04(self): self.performTest4(loadJSON("tests/read/containerkind/test4.json"))
    def test_containerkind_read_XML04(self):  self.performTest4(loadXML("tests/read/containerkind/test4.xml"))
    def test_containerkind_read_YAML04(self): self.performTest4(loadYAML("tests/read/containerkind/test4.yaml"))

    def performTest5(self, instance):
        self.test_instance.containerkinds[0].loadingspaces = list()
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON05(self): self.performTest5(loadJSON("tests/read/containerkind/test5.json"))
    def test_containerkind_read_XML05(self):  self.performTest5(loadXML("tests/read/containerkind/test5.xml"))
    def test_containerkind_read_YAML05(self): self.performTest5(loadYAML("tests/read/containerkind/test5.yaml"))

    def performTest6(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].id = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON06(self): self.performTest6(loadJSON("tests/read/containerkind/test6.json"))
    def test_containerkind_read_XML06(self):  self.performTest6(loadXML("tests/read/containerkind/test6.xml"))
    def test_containerkind_read_YAML06(self): self.performTest6(loadYAML("tests/read/containerkind/test6.yaml"))

    def performTest7(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].position = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON07(self): self.performTest7(loadJSON("tests/read/containerkind/test7.json"))
    def test_containerkind_read_XML07(self):  self.performTest7(loadXML("tests/read/containerkind/test7.xml"))
    def test_containerkind_read_YAML07(self): self.performTest7(loadYAML("tests/read/containerkind/test7.yaml"))

    def performTest8(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].boundingBox = [None, None, None]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON08(self): self.performTest8(loadJSON("tests/read/containerkind/test8.json"))
    def test_containerkind_read_XML08(self):  self.performTest8(loadXML("tests/read/containerkind/test8.xml"))
    def test_containerkind_read_YAML08(self): self.performTest8(loadYAML("tests/read/containerkind/test8.yaml"))

    def performTest9(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].boundingBox = [None, 1000, 1000]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON09(self): self.performTest9(loadJSON("tests/read/containerkind/test9.json"))
    def test_containerkind_read_XML09(self):  self.performTest9(loadXML("tests/read/containerkind/test9.xml"))
    def test_containerkind_read_YAML09(self): self.performTest9(loadYAML("tests/read/containerkind/test9.yaml"))

    def performTest10(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].boundingBox = [2000, None, 1000]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON10(self): self.performTest10(loadJSON("tests/read/containerkind/test10.json"))
    def test_containerkind_read_XML10(self):  self.performTest10(loadXML("tests/read/containerkind/test10.xml"))
    def test_containerkind_read_YAML10(self): self.performTest10(loadYAML("tests/read/containerkind/test10.yaml"))

    def performTest11(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].boundingBox = [2000, 1000, None]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON11(self): self.performTest11(loadJSON("tests/read/containerkind/test11.json"))
    def test_containerkind_read_XML11(self):  self.performTest11(loadXML("tests/read/containerkind/test11.xml"))
    def test_containerkind_read_YAML11(self): self.performTest11(loadYAML("tests/read/containerkind/test11.yaml"))

    def performTest12(self, instance):
        self.test_instance.containerkinds[0].id = "1a"
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON12(self): self.performTest12(loadJSON("tests/read/containerkind/test12.json"))
    def test_containerkind_read_XML12(self):  self.performTest12(loadXML("tests/read/containerkind/test12.xml"))
    def test_containerkind_read_YAML12(self): self.performTest12(loadYAML("tests/read/containerkind/test12.yaml"))
    
    def performTest13(self, instance):
        self.test_instance.containerkinds[0].loadingspaces[0].position = ["0a","0","0"]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_containerkind_read_JSON13(self): self.performTest13(loadJSON("tests/read/containerkind/test13.json"))
    def test_containerkind_read_XML13(self):  self.performTest13(loadXML("tests/read/containerkind/test13.xml"))
    def test_containerkind_read_YAML13(self): self.performTest13(loadYAML("tests/read/containerkind/test13.yaml"))

class TestReadPalletkind(unittest.TestCase):
    def setUp(self):
        self.test_instance = ThreeDinstance()
        self.test_instance.description.setname = "Palletkind"
        self.test_instance.description.name    = "Test"
        pallet_kind = ThreeDpalletkind()
        pallet_kind.id = 1
        pallet_kind.quantity = 1
        pallet_kind.boundingBox = [1000, 1000, 10]
        pallet_kind.position = [0, 0, 0]
        pallet_kind.orientations = set(['LWH','WLH'])
        self.test_instance.addPalletkind(pallet_kind)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [1000, 1000, 1500]
        loadingspace.position = [0, 0, 10]
        pallet_kind.loadingspace = loadingspace
        pallet_kind = ThreeDpalletkind()
        pallet_kind.id = 2
        pallet_kind.quantity = 9999
        pallet_kind.boundingBox = [1000, 1000, 100]
        pallet_kind.position = [0, 0, 0]
        pallet_kind.orientations = set(['LWH','WLH'])
        self.test_instance.addPalletkind(pallet_kind)
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [1000, 1000, 1000]
        loadingspace.position = [0, 0, 100]
        pallet_kind.loadingspace = loadingspace

    def performTest1(self, instance):
        self.assertEqual(instance, self.test_instance)
        self.assertTrue(instance.IsValid()[0])
    def test_palletkind_read_JSON01(self): self.performTest1(loadJSON("tests/read/palletkind/test1.json"))
    def test_palletkind_read_XML01(self):  self.performTest1(loadXML("tests/read/palletkind/test1.xml"))
    def test_palletkind_read_YAML01(self): self.performTest1(loadYAML("tests/read/palletkind/test1.yaml"))

    def performTest2(self, instance):
        self.test_instance.palletkinds[0].id = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON02(self): self.performTest2(loadJSON("tests/read/palletkind/test2.json"))
    def test_palletkind_read_XML02(self):  self.performTest2(loadXML("tests/read/palletkind/test2.xml"))
    def test_palletkind_read_YAML02(self): self.performTest2(loadYAML("tests/read/palletkind/test2.yaml"))

    def performTest3(self, instance):
        self.test_instance.palletkinds[0].quantity = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON03(self): self.performTest3(loadJSON("tests/read/palletkind/test3.json"))
    def test_palletkind_read_XML03(self):  self.performTest3(loadXML("tests/read/palletkind/test3.xml"))
    def test_palletkind_read_YAML03(self): self.performTest3(loadYAML("tests/read/palletkind/test3.yaml"))

    def performTest4(self, instance):
        self.test_instance.palletkinds[0].position = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON04(self): self.performTest4(loadJSON("tests/read/palletkind/test4.json"))
    def test_palletkind_read_XML04(self):  self.performTest4(loadXML("tests/read/palletkind/test4.xml"))
    def test_palletkind_read_YAML04(self): self.performTest4(loadYAML("tests/read/palletkind/test4.yaml"))

    def performTest5(self, instance):
        self.test_instance.palletkinds[0].boundingBox = [None, None, None]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON05(self): self.performTest5(loadJSON("tests/read/palletkind/test5.json"))
    def test_palletkind_read_XML05(self):  self.performTest5(loadXML("tests/read/palletkind/test5.xml"))
    def test_palletkind_read_YAML05(self): self.performTest5(loadYAML("tests/read/palletkind/test5.yaml"))

    def performTest6(self, instance):
        self.test_instance.palletkinds[0].boundingBox = [None, 1000, 10]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON06(self): self.performTest6(loadJSON("tests/read/palletkind/test6.json"))
    def test_palletkind_read_XML06(self):  self.performTest6(loadXML("tests/read/palletkind/test6.xml"))
    def test_palletkind_read_YAML06(self): self.performTest6(loadYAML("tests/read/palletkind/test6.yaml"))

    def performTest7(self, instance):
        self.test_instance.palletkinds[0].boundingBox = [1000, None, 10]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON07(self): self.performTest7(loadJSON("tests/read/palletkind/test7.json"))
    def test_palletkind_read_XML07(self):  self.performTest7(loadXML("tests/read/palletkind/test7.xml"))
    def test_palletkind_read_YAML07(self): self.performTest7(loadYAML("tests/read/palletkind/test7.yaml"))

    def performTest8(self, instance):
        self.test_instance.palletkinds[0].boundingBox = [1000, 1000, None]
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON08(self): self.performTest8(loadJSON("tests/read/palletkind/test8.json"))
    def test_palletkind_read_XML08(self):  self.performTest8(loadXML("tests/read/palletkind/test8.xml"))
    def test_palletkind_read_YAML08(self): self.performTest8(loadYAML("tests/read/palletkind/test8.yaml"))

    def performTest9(self, instance):
        self.test_instance.palletkinds[0].orientations = None
        self.assertEqual(instance, self.test_instance)
        self.assertFalse(instance.IsValid()[0])
    def test_palletkind_read_JSON09(self): self.performTest9(loadJSON("tests/read/palletkind/test9.json"))
    def test_palletkind_read_XML09(self):  self.performTest9(loadXML("tests/read/palletkind/test9.xml"))
    def test_palletkind_read_YAML09(self): self.performTest9(loadYAML("tests/read/palletkind/test9.yaml"))
    
TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReadDescription))
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReadContainerkind))
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReadPalletkind))