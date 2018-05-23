from ..common.Requirements import BaseRequirement, BaseConstraint
from ..common.utils import indent

class ThreeDconstraint(object):
    CONSTRAINTS = sorted([c.name for c in BaseRequirement.CONSTRAINT_LIST])
    
    def __init__(self):
        self.constraint = BaseConstraint()
        
    def IsValid(self):
        errors = [""]
        if self.constraint is None or isinstance(self.constraint, BaseConstraint) or not issubclass(self.constraint, BaseConstraint):
            errors.append("Expected constraint")
        elif self.constraint.name is None:
            errors.append("Constraint name undefined")
        elif not isinstance(self.constraint.name, str):
            errors.append("Constraint name should be a string")
        elif self.constraint.name not in self.CONSTRAINTS:
            errors.append("Constraint name not found")
            
        if len(errors)>1:
            return False, "Invalid constraint:" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "constraint"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and isinstance(self.constraint, type(other.constraint))
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")