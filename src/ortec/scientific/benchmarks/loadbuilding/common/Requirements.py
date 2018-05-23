from .utils import flatten
import pkgutil
import os
import importlib

class Requirements(object):
    def __init__(self):
        self.warnings = list()
        self.valid = True

    # Calling this function will update the current requirements report on whether the existence requirement is met
    def RequireExists(self, field, req):
        if not hasattr(field, req.field):
            setattr(field, req.field, None)
        if getattr(field, req.field) is None:
            warning = "No " + str(req.field) + " defined for " + field.TypeString() + " with id " + str(field.id)
            if req.default is None:
                warning += ", please specify"
                self.valid = False
            else:
                warning += ", setting to " + str(req.default)
                setattr(field, req.field, req.default)
            self.warnings.append(warning)
        elif req.cast(getattr(field, req.field)) != getattr(field, req.field):
            print(type(getattr(field, req.field)))
            self.warnings.append("Expected " + str(req.field) + " of " + field.TypeString() + " to be of type " + req.cast.__name__ + ", but got " + type(getattr(field, req.field)).__name__)
            self.valid = False
            
    # Calling this function will update the current requirements report on whether the proposition requirement is met
    def RequireProposition(self, field, req):
        if not hasattr(field, req.field):
            setattr(field, req.field, None)    
        if getattr(field, req.field) is None:
            self.valid = False
        else:
            try:
                if not req.prop(getattr(field, req.field)):
                    self.warnings.append("For " + field.TypeString() + " with kind id " + str(field.id) + ", " + req.error)
                    self.valid = False
            except Exception:
                self.warnings.append("Exception caught when checking proposition")
                self.valid = False
    
    # Imposes the given requirements on the given fields
    def addRequirements(self, reqs, fields):
        for req in reqs:
            for tf in fields:
                if isinstance(req, ExistenceRequirement):
                    self.RequireExists(tf, req)
                elif isinstance(req, PropositionalRequirement):
                    self.RequireProposition(tf, req)
    
    # Return the current warning report
    def getWarnings(self):
        return "\n".join(self.warnings)

class ExistenceRequirement(object):
    def __init__(self,field,default,cast):
        self.field = field
        self.default = default
        self.cast = cast
    def __str__(self):
        string = str(self.field) + " of type " + self.cast.__name__
        if self.default is not None:
            string += " with default value " + str(self.default)
        return string

class PropositionalRequirement(object):
    def __init__(self,field,prop,error):
        self.field = field
        self.prop = prop
        self.error = error
    def __str__(self):
        return str(self.error)

# Used for checking whether all defaults match for all fields in the Constraints and Objectives files
itemkindDefaults      = dict()
boxkindDefaults       = dict()
palletkindDefaults    = dict()
containerkindDefaults = dict()
loadingspaceDefaults  = dict()
    
class BaseRequirement(type):
    OBJECTIVE_LIST  = []
    CONSTRAINT_LIST = []
    
    itemkindRequirements      = []
    boxkindRequirements       = []
    palletkindRequirements    = []
    containerkindRequirements = []
    loadingspaceRequirements  = []
    @staticmethod
    def IsObjective():
        return False
    @staticmethod
    def IsConstraint():
        return False
    
    @classmethod
    # BaseRequirement, BaseConstraint, and BaseObjective are not added to the CONSTRAINT_LIST or OBJECTIVE_LIST
    def _IsActiveRequirement_(c,cls):
        return len(cls.mro()) > 2 
    
    # By meta-classing, each time we derive from BaseRequirement, BaseConstraint, or BaseObjective, the __init__ method is called
    # We add a check that ensures that all default values for the ExistenceRequirements match each other
    def __init__(cls, name, bases, clsdict):
        if cls._IsActiveRequirement_(cls):
            for f,d,c in [(req.field, req.default, req.cast) for req in cls.itemkindRequirements if isinstance(req, ExistenceRequirement)]:
                if d is None:
                    casted = None
                else:
                    casted = c(d)
                if f in itemkindDefaults:
                    if itemkindDefaults[f] != casted:
                        raise Exception("Expected " + str(itemkindDefaults[f]) + " as default for " + str(f) + " in " + str(cls.__name__))
                else:
                    itemkindDefaults[f] = casted
            for f,d,c in [(req.field, req.default, req.cast) for req in cls.containerkindRequirements if isinstance(req, ExistenceRequirement)]:
                if d is None:
                    casted = None
                else:
                    casted = c(d)
                if f in containerkindDefaults:
                    if containerkindDefaults[f] != casted:
                         raise Exception("Expected " + str(containerkindDefaults[f]) + " as default for " + str(f) + " in " + str(cls.__name__))
                else:
                    containerkindDefaults[f] = casted
            for f,d,c in [(req.field, req.default, req.cast) for req in cls.loadingspaceRequirements if isinstance(req, ExistenceRequirement)]:
                if d is None:
                    casted = None
                else:
                    casted = c(d)
                if f in loadingspaceDefaults:
                    if loadingspaceDefaults[f] != casted:
                        raise Exception("Expected " + str(loadingspaceDefaults[f]) + " as default for " + str(f) + " in " + str(cls.__name__))
                else:
                    loadingspaceDefaults[f] = casted
            if cls.IsObjective():
                BaseRequirement.OBJECTIVE_LIST.append(cls)
            if cls.IsConstraint():
                BaseRequirement.CONSTRAINT_LIST.append(cls)
        super(BaseRequirement, cls).__init__(name, bases, clsdict)
    
    # Test whether all requirements are met in a given ThreeDinstance object
    def TestDataRequirements(self,threeDinstance):
        r = Requirements()
        r.addRequirements(self.itemkindRequirements,      threeDinstance.itemkinds)
        r.addRequirements(self.boxkindRequirements,       threeDinstance.boxkinds)
        r.addRequirements(self.palletkindRequirements,    threeDinstance.palletkinds)
        r.addRequirements(self.containerkindRequirements, threeDinstance.containerkinds)
        r.addRequirements(self.loadingspaceRequirements,  flatten([c.loadingspaces for c in threeDinstance.containerkinds]))
        return r.valid, r.getWarnings()

# When implementing a base class that should not be listed in the OBJECTIVE_LIST,
# use the following template (not tested with multiple inheritance):
#
#  class ____Objective(superclass):
#      ...
#
#      @classmethod
#      def _IsActiveRequirement_(c,cls):
#          return len(cls.mro()) > len(superclass.mro()) + 1
class BaseObjective(metaclass = BaseRequirement):
    name = ""
    @staticmethod
    def IsObjective():
        return True
    def Evaluate(threeDinstance):
        raise Exception("Derived classes of BaseObjective need to override the Evaluate-method")
        
# When implementing a base class that should not be listed in the CONSTRAINT_LIST,
# use the following template (not tested with multiple inheritance):
#
#  class ____Constraint(superclass):
#      ...
#
#      @classmethod
#      def _IsActiveRequirement_(c,cls):
#          return len(cls.mro()) > len(superclass.mro()) + 1
class BaseConstraint(metaclass = BaseRequirement):
    name = ""
    @staticmethod
    def IsConstraint():
        return True
    def Validate(threeDinstance):
        raise Exception("Derived classes of BaseConstraint need to override the Validate-method")


def import_all_modules_from_dir(dirname):
    path = os.path.join(os.path.dirname(__file__),dirname)
    for (_, name, _) in pkgutil.iter_modules([path]):
        importlib.import_module('.' + dirname + '.' + name, __package__)
        
        
import_all_modules_from_dir('constraints')
import_all_modules_from_dir('objectives')

if __name__=="__main__":
    exit("Don't run this file")
    