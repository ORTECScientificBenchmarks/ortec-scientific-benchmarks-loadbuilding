import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDinstance import ThreeDinstance
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDcontainerkind import ThreeDcontainerkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDpalletkind    import ThreeDpalletkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDboxkind       import ThreeDboxkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDitemkind      import ThreeDitemkind
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDloadingspace  import ThreeDloadingspace
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDconstraint    import ThreeDconstraint
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDobjective     import ThreeDobjective
from ortec.scientific.benchmarks.loadbuilding.common.constraints.MaximumWeightConstraint import MaximumWeightConstraint as MaximumWeightConstraint
from ortec.scientific.benchmarks.loadbuilding.common.objectives.ItemCountObjective import ItemCountObjective

class TestInstance(unittest.TestCase):
    def setUp(self):
        self.instance = ThreeDinstance()
        self.instance.description.setname = "Instance"
        self.instance.description.name    = "Test"
        
    def test_instance_valid(self):
        self.assertTrue(self.instance.IsValid()[0])

    def test_instance_addcontainerkind(self):
        container_kind = ThreeDcontainerkind()
        container_kind.id = 1
        container_kind.quantity = 1
        loadingspace = ThreeDloadingspace()
        loadingspace.id = 1
        loadingspace.boundingBox = [2000, 1000, 1000]
        loadingspace.position = [0, 0, 0]
        container_kind.addLoadingspace(loadingspace)
        self.instance.addContainerkind(container_kind)
        self.assertEqual(len(self.instance.containerkinds), 1)
        self.assertTrue(self.instance.IsValid()[0])

    def test_instance_addpalletkind(self):
        pallet_kind = ThreeDpalletkind()
        pallet_kind.id = 1
        pallet_kind.quantity = 1
        pallet_kind.boundingBox = [750, 750, 10]
        pallet_kind.position = [0, 0, 0]
        pallet_kind.loadingspace = ThreeDloadingspace()
        pallet_kind.loadingspace.id = 1
        pallet_kind.loadingspace.boundingBox = [750, 750, 1500]
        pallet_kind.loadingspace.position = [0, 0, 10]
        pallet_kind.orientations = set(['LWH', 'WLH'])
        self.instance.addPalletkind(pallet_kind)
        self.assertEqual(len(self.instance.palletkinds), 1)
        self.assertTrue(self.instance.IsValid()[0])
    
    def test_instance_addboxkind(self):
        box_kind = ThreeDboxkind()
        box_kind.id = 1
        box_kind.quantity = 1
        box_kind.boundingBox = [750, 750, 10]
        box_kind.position = [0, 0, 0]
        box_kind.loadingspace = ThreeDloadingspace()
        box_kind.loadingspace.id = 1
        box_kind.loadingspace.boundingBox = [750, 750, 1500]
        box_kind.loadingspace.position = [0, 0, 10]
        box_kind.orientations = set(['LWH', 'WLH'])
        self.instance.addBoxkind(box_kind)
        self.assertEqual(len(self.instance.boxkinds), 1)
        self.assertTrue(self.instance.IsValid()[0])

    def test_instance_additemkind(self):
        item_kind = ThreeDitemkind()
        item_kind.id = 1
        item_kind.quantity = 10
        item_kind.boundingBox = [10,10,10]
        item_kind.orientations = set(['LWH', 'WLH'])
        self.instance.addItemkind(item_kind)
        self.assertEqual(len(self.instance.itemkinds), 1)
        self.assertTrue(self.instance.IsValid()[0])

    def test_instance_addconstraint(self):
        constraint = ThreeDconstraint()
        constraint.constraint = MaximumWeightConstraint
        self.instance.addConstraint(constraint)
        self.assertEqual(len(self.instance.constraints), 1)
        self.assertTrue(self.instance.IsValid()[0])
    
    def test_instance_addobjective(self):
        objective = ThreeDobjective()
        objective.objective = ItemCountObjective
        objective.priority = 1
        objective.weight   = 1.0
        self.instance.addObjective(objective)
        self.assertEqual(len(self.instance.objectives), 1)
        self.assertTrue(self.instance.IsValid()[0])

    def test_instance_isdatacomplete1(self):
        pass

    def test_instance_typestring(self):
        self.assertEqual(self.instance.TypeString(), "instance")
        
    def test_instance_ne(self):
        self.assertNotEqual(self.instance, ThreeDinstance())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestInstance))