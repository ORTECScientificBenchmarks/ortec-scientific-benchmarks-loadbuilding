from ..common.Requirements import BaseRequirement, BaseObjective
from ..common.utils import indent

class ThreeDobjective(object):
    OBJECTIVES = sorted([o.name for o in BaseRequirement.OBJECTIVE_LIST])
    
    def __init__(self):
        self.objective = BaseObjective()
        self.priority  = None
        self.weight    = None
        
    def IsValid(self):
        errors = [""]
        
        if self.objective is None or isinstance(self.objective, BaseObjective) or not issubclass(self.objective, BaseObjective):
            errors.append("Expected objective")
        elif self.objective.name is None:
            errors.append("Objective name undefined")
        elif not isinstance(self.objective.name, str):
            errors.append("Objective name should be a string")
        elif self.objective.name not in self.OBJECTIVES:
            errors.append("Objective name not found")
            
        if self.priority is None:
            errors.append("Priority undefined")
        elif not isinstance(self.priority, int):
            errors.append("Priority should be integer")
        elif not self.priority > 0:
            errors.append("Priority should be positive")
            
        if self.weight is None:
            errors.append("Weight undefined")
        elif not isinstance(self.weight, float):
            errors.append("Weight should be float")
        elif not self.weight > 0.0:
            errors.append("Weight should be positive")
        
        if len(errors)>1:
            return False, "Invalid objective:" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "objective"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and isinstance(self.objective, type(other.objective)) and self.priority == other.priority and self.weight == other.weight
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")