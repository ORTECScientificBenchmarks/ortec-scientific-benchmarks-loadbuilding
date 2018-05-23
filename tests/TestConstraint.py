import unittest
from ortec.scientific.benchmarks.loadbuilding.instance.ThreeDconstraint                         import ThreeDconstraint
from ortec.scientific.benchmarks.loadbuilding.common.constraints.MaximumWeightConstraint        import MaximumWeightConstraint as MaximumWeightConstraint

class TestConstraint(unittest.TestCase):
    def setUp(self):
        self.constraint = ThreeDconstraint()
        self.constraint.constraint = MaximumWeightConstraint

    def test_constraint_valid(self):
        self.assertTrue(self.constraint.IsValid()[0])
    
    def test_constraint_typestring(self):
        self.assertEqual(self.constraint.TypeString(), "constraint")
        
    def test_constraint_ne(self):
        self.assertNotEqual(self.constraint, ThreeDconstraint())

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestConstraint))