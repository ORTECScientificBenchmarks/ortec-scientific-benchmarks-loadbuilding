import unittest
import os

from ortec.scientific.benchmarks.loadbuilding.instance.read.XMLtoThreeDinstance  import XMLtoThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.solution.read.JSONtoThreeDsolution import JSONtoThreeDsolution
from ortec.scientific.benchmarks.loadbuilding.solution.read.XMLtoThreeDsolution  import XMLtoThreeDsolution
from ortec.scientific.benchmarks.loadbuilding.solution.read.YAMLtoThreeDsolution import YAMLtoThreeDsolution

from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDinstance      import ThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDcontainerkind import ThreeDcontainerkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDitemkind      import ThreeDitemkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace  import ThreeDloadingspace as instLoadingspace
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDsolution      import ThreeDsolution
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDcontainer     import ThreeDcontainer
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDplacement     import ThreeDplacement
from ortec.scientific.benchmarks.loadbuilding.solution.ThreeDloadingspace  import ThreeDloadingspace as solLoadingspace

def getfilename(name):
    return os.path.join(os.path.dirname(__file__),'..',name)

def loadJSON(instancename, solutionname):
    instance = XMLtoThreeDinstance(getfilename(instancename)).CreateThreeDinstance()
    return JSONtoThreeDsolution(getfilename(solutionname)).CreateThreeDsolution(instance)

def loadXML(instancename, solutionname):
    instance = XMLtoThreeDinstance(getfilename(instancename)).CreateThreeDinstance()
    return XMLtoThreeDsolution(getfilename(solutionname)).CreateThreeDsolution(instance)

def loadYAML(instancename, solutionname):
    instance = XMLtoThreeDinstance(getfilename(instancename)).CreateThreeDinstance()
    return YAMLtoThreeDsolution(getfilename(solutionname)).CreateThreeDsolution(instance)
    
class TestReadContainer(unittest.TestCase):
    def setUp(self):
        self.test_instance = ThreeDinstance()
        self.test_instance.description.setname = "Container"
        self.test_instance.description.name    = "Test"
        container_kind = ThreeDcontainerkind()
        container_kind.id = 1
        container_kind.quantity = 1
        self.test_instance.addContainerkind(container_kind)
        loadingspace = instLoadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [0, 0, 0]
        container_kind.addLoadingspace(loadingspace)
        loadingspace = instLoadingspace()
        loadingspace.id = 2
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [2000, 0, 0]
        container_kind.addLoadingspace(loadingspace)
        item_kind = ThreeDitemkind()
        item_kind.id = 1
        item_kind.quantity = 4
        item_kind.boundingBox = [500, 500, 500]
        item_kind.orientations = set(["LWH","lwH","WlH","wLH"])
        self.test_instance.addItemkind(item_kind)
        self.test_solution = ThreeDsolution(self.test_instance)
        self.test_solution.description.setname = "Container"
        self.test_solution.description.name = "Test"
        container = ThreeDcontainer()
        container.id = 1
        container.kindid = 1
        loadingspace = solLoadingspace()
        loadingspace.id = 1
        loadingspace.placements = []
        placement = ThreeDplacement()
        placement.id = 1
        placement.itemid = 1
        placement.position = [0,0,0]
        placement.orientation = "LWH"
        loadingspace.placements.append(placement)
        placement = ThreeDplacement()
        placement.id = 2
        placement.itemid = 1
        placement.position = [0,0,500]
        placement.orientation = "LWH"
        loadingspace.placements.append(placement)
        placement = ThreeDplacement()
        placement.id = 3
        placement.itemid = 1
        placement.position = [0,500,0]
        placement.orientation = "LWH"
        loadingspace.placements.append(placement)
        container.addLoadingspace(loadingspace)
        self.test_solution.addContainer(container)
        self.test_solution.unplaced = []
        placement = ThreeDplacement()
        placement.id = 4
        placement.itemid = 1
        placement.quantity = 1
        placement.position = "UNPLACED"
        placement.orientation = "UNPLACED"
        placement.type = None
        self.test_solution.unplaced.append(placement)

    def performTest1(self, solution):
        self.assertEqual(solution, self.test_solution)
        self.assertTrue(solution.IsValid()[0])
    def test_container_read_JSON01(self): self.performTest1(loadJSON("tests/read/container/inst.xml", "tests/read/container/test1.json"))
    def test_container_read_XML01(self):  self.performTest1(loadXML("tests/read/container/inst.xml", "tests/read/container/test1.xml"))
    def test_container_read_YAML01(self): self.performTest1(loadYAML("tests/read/container/inst.xml", "tests/read/container/test1.yaml"))

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReadContainer))