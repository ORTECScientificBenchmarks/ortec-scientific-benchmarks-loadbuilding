import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDobjective import ThreeDobjective
from ortec.scientific.benchmarks.loadbuilding.common.objectives.ItemCountObjective        import ItemCountObjective
    
class TestObjective(unittest.TestCase):
    def setUp(self):
        self.objective = ThreeDobjective()
        self.objective.objective = ItemCountObjective
        self.objective.priority = 1
        self.objective.weight   = 1.0

    def test_objective_valid(self):
        self.assertTrue(self.objective.IsValid()[0])

    def test_objective_invalid_priority1(self):
        self.objective.priority = None
        self.assertFalse(self.objective.IsValid()[0])
    def test_objective_invalid_priority2(self):
        self.objective.priority = "1"
        self.assertFalse(self.objective.IsValid()[0])
    def test_objective_invalid_priority3(self):
        self.objective.priority = -1
        self.assertFalse(self.objective.IsValid()[0])
            
    def test_objective_invalid_weight1(self):
        self.objective.weight = None
        self.assertFalse(self.objective.IsValid()[0])
    def test_objective_invalid_weight2(self):
        self.objective.weight = "1.0"
        self.assertFalse(self.objective.IsValid()[0])
    def test_objective_invalid_weight3(self):
        self.objective.weight = -1.0
        self.assertFalse(self.objective.IsValid()[0])
    
    def test_objective_typestring(self):
        self.assertEqual(self.objective.TypeString(), "objective")
        
    def test_objective_ne(self):
        self.assertNotEqual(self.objective, ThreeDobjective())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestObjective))