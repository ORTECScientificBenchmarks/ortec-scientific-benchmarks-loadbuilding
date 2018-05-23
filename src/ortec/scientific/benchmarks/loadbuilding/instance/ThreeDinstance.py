from ..common.Requirements import BaseRequirement
from ..common.utils import key, combine, checkDuplicateIds, checkDuplicateNames, flatten, Report

from .ThreeDdescription   import ThreeDdescription
from .ThreeDcontainerkind import ThreeDcontainerkind
from .ThreeDpalletkind    import ThreeDpalletkind
from .ThreeDboxkind       import ThreeDboxkind
from .ThreeDitemkind      import ThreeDitemkind
from .ThreeDconstraint    import ThreeDconstraint
from .ThreeDobjective     import ThreeDobjective

class ThreeDinstance(object):
    def __init__(self):
        self.description    = ThreeDdescription()
        self.containerkinds = list()
        self.palletkinds    = list()
        self.boxkinds       = list()
        self.itemkinds      = list()
        self.constraints    = list()
        self.objectives     = list()
        
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        self.sort()
        other.sort()
        return self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
    def addContainerkind(self, containerkind):
        if not isinstance(containerkind, ThreeDcontainerkind):
            raise Exception("Expected a containerkind")
        self.containerkinds.append(containerkind)
    
    def addPalletkind(self, palletkind):
        if not isinstance(palletkind, ThreeDpalletkind):
            raise Exception("Expected a palletkind")
        self.palletkinds.append(palletkind)
    
    def addBoxkind(self, boxkind):
        if not isinstance(boxkind, ThreeDboxkind):
            raise Exception("Expected a boxkind")
        self.boxkinds.append(boxkind)
    
    def addItemkind(self, itemkind):
        if not isinstance(itemkind, ThreeDitemkind):
            raise Exception("Expected an itemkind")
        self.itemkinds.append(itemkind)
    
    def addConstraint(self, constraint):
        if not isinstance(constraint, ThreeDconstraint):
            raise Exception("Expected a constraint")
        self.constraints.append(constraint)
    
    def addObjective(self, objective):
        if not isinstance(objective, ThreeDobjective):
            raise Exception("Expected an objective")
        self.objectives.append(objective)
    
    # Checks whether the necessary data is well-formed
    def IsValid(self):
        report = Report()
        report.add(self.description.IsValid())
        report.add(checkDuplicateIds(self.containerkinds))
        report.add(checkDuplicateIds(self.palletkinds))
        report.add(checkDuplicateIds(self.boxkinds))
        report.add(checkDuplicateIds(self.itemkinds))
        report.add(checkDuplicateNames([c.constraint for c in self.constraints if hasattr(c, "constraint")]))
        
        lists_to_check = [self.containerkinds, self.palletkinds, self.boxkinds, self.itemkinds, self.constraints, self.objectives]
        for ltc in lists_to_check:
            for element in ltc:
                if element is not None:
                    report.add(element.IsValid())
                else:
                    report.add((False, "Unexpected occurrence of None"))
        return report.get()
    
    # Checks whether all requirements are met
    def IsDataComplete(self):
        report = Report()
        for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
            if r.name in [o.objective.name for o in self.objectives] + [c.constraint.name for c in self.constraints]:
                report.add(r.TestDataRequirements(self), fail=False, verbose=False)
        return report.get()
    
    # Checks whether there are fields defined that are not needed to satisfy the requirements of the constraints and objectives
    def TooMuchData(self, remove_unused):
        warnings = list()
        unusedItemFields, unusedBoxFields, unusedPalletFields, unusedContainerFields,  unusedLoadingspaceFields  = set(), set(), set(), set(), set()
        for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
            unusedItemFields         |= set([req.field for req in r.itemkindRequirements])
            unusedBoxFields          |= set([req.field for req in r.boxkindRequirements])
            unusedPalletFields       |= set([req.field for req in r.palletkindRequirements])
            unusedContainerFields    |= set([req.field for req in r.containerkindRequirements])
            unusedLoadingspaceFields |= set([req.field for req in r.loadingspaceRequirements])
        for c in self.constraints:
            for r in BaseRequirement.CONSTRAINT_LIST:
                if c.constraint.name != r.name:
                    continue
                unusedItemFields         -= set([req.field for req in r.itemkindRequirements])
                unusedBoxFields          -= set([req.field for req in r.boxkindRequirements])
                unusedPalletFields       -= set([req.field for req in r.palletkindRequirements])
                unusedContainerFields    -= set([req.field for req in r.containerkindRequirements])
                unusedLoadingspaceFields -= set([req.field for req in r.loadingspaceRequirements])
                break
        for o in self.objectives:
            for r in BaseRequirement.OBJECTIVE_LIST:
                if o.objective.name != r.name:
                    continue
                unusedItemFields         -= set([req.field for req in r.itemkindRequirements])
                unusedBoxFields          -= set([req.field for req in r.boxkindRequirements])
                unusedPalletFields       -= set([req.field for req in r.palletkindRequirements])
                unusedContainerFields    -= set([req.field for req in r.containerkindRequirements])
                unusedLoadingspaceFields -= set([req.field for req in r.loadingspaceRequirements])
                break
        for uif in unusedItemFields:
            for i in self.itemkinds:
                if hasattr(i,uif) and getattr(i,uif) is not None:
                    if remove_unused:
                        warnings.append("Removed unused " + uif + " for itemkind with id " + str(i.id))
                        delattr(i, uif)
                    else:
                        warnings.append("Unused " + uif + " for itemkind with id " + str(i.id))
        for ubf in unusedBoxFields:
            for b in self.boxkinds:
                if hasattr(b,ubf) and getattr(b,ubf) is not None:
                    if remove_unused:
                        warnings.append("Removed unused " + ubf + " for boxkind with id " + str(b.id))
                        delattr(b, ubf)
                    else:
                        warnings.append("Unused " + ubf + " for boxkind with id " + str(b.id))
        for upf in unusedPalletFields:
            for p in self.palletkinds:
                if hasattr(p,upf) and getattr(p,upf) is not None:
                    if remove_unused:
                        warnings.append("Removed unused " + upf + " for palletkind with id " + str(p.id))
                        delattr(p, upf)
                    else:
                        warnings.append("Unused " + upf + " for palletkind with id " + str(p.id))
        for ucf in unusedContainerFields:
            for c in self.containerkinds:
                if hasattr(c,ucf) and getattr(c, ucf) is not None:
                    if remove_unused:
                        warnings.append("Removed unused " + ucf + " for containerkind with id " + str(c.id))
                        delattr(c, ucf)
                    else:
                        warnings.append("Unused " + ucf + " for containerkind with id " + str(c.id))
        for ulf in unusedLoadingspaceFields:
            for l in self.GetAllLoadingspaces():
                if hasattr(l,ulf) and getattr(l, ulf) is not None:
                    if remove_unused:
                        warnings.append("Removed unused " + ulf + " for loadingspace with id " + str(l.id))
                        delattr(l, ulf)
                    else:
                        warnings.append("Unused " + ulf + " for loadingspace with id " + str(l.id))
        return True, "\n".join(warnings)
    
    def CountMultiples(self):
        warnings  = list()
        to_remove = list()
        for n,i in enumerate(self.itemkinds):
            for m,j in enumerate(self.itemkinds[n+1:]):
                if n+m+1 not in to_remove and {x: i.__dict__[x] for x in i.__dict__ if x not in ['id', 'quantity']} == {x: j.__dict__[x] for x in j.__dict__ if x not in ['id', 'quantity']}:
                    i.quantity += j.quantity
                    to_remove.append(n+m+1)
                    warnings.append("Removed duplicate of item with id " + str(i.id) + ": item with id " + str(j.id))
        self.itemkinds = [i for n,i in enumerate(self.itemkinds) if n not in to_remove]
        return True, "\n".join(warnings)
    
    # Changes all ids of containerkinds, palletkinds, boxkinds, their loadingspaces, and itemkinds by mapping them to the lowest possible positive integers that preserve their ordering
    # The same happens for the priorities of the objectives
    def Reindex(self):
        warnings = list()
        lists_to_check = [self.containerkinds, self.palletkinds, self.boxkinds, self.itemkinds]
        for ltc in lists_to_check:
            for n,element in enumerate(ltc):
                if element.id != n+1:
                    warnings.append("Changed id of " + element.TypeString() + ": " + str(element.id) + " -> " + str(n+1))
                    element.id = n+1
                if hasattr(element, "loadingspaces"):
                    for n,ls in enumerate(element.loadingspaces):
                        if ls.id != n+1:
                            warnings.append("Changed id of loadingspace of " + element.TypeString() + " with id " + str(element.id) + ": " + str(ls.id) + " -> " + str(n+1))
                            ls.id = n+1
        if self.objectives:
            current_priority = self.objectives[0].priority
            new_priority = 1
            for o in self.objectives:
                if o.priority > current_priority:
                    current_priority = o.priority
                    new_priority += 1
                if o.priority != new_priority:
                    warnings.append("Changed priority of objective " + str(o.objective.name) + ": " + str(o.priority) + " -> " + str(new_priority))
                    o.priority = new_priority
        return True, "\n".join(warnings)
    
    def sort(self):
        if self.itemkinds != None:
            self.itemkinds.sort(key=key("id"))
        if self.boxkinds != None:
            self.boxkinds.sort(key=key("id"))
        if self.palletkinds != None:
            self.palletkinds.sort(key=key("id"))
        if self.containerkinds != None:
            self.containerkinds.sort(key=key("id"))
            for containerkind in self.containerkinds:
                if containerkind != None:
                    containerkind.sort()
        if self.objectives != None:
            self.objectives.sort(key=combine([key("priority"), lambda x: key("name")(key("objective", None)(x)), key("weight")]))
        if self.constraints != None:
            self.constraints.sort(key=lambda x: key("name")(key("constraint", None)(x)))
    
    @staticmethod
    def TypeString():
        return "instance"
    
    def GetAllLoadingspaces(self):
        return sorted(flatten([c.loadingspaces for c in self.containerkinds]), key=lambda x: x.id)
    
    def AllChecks(self, reindex=False, remove_unused=False):
        report = Report()
        report.add(self.IsValid(), verbose=True, fail=True)
        self.sort()
        report.add(self.CountMultiples(), verbose=True)
        report.add(self.IsDataComplete(), verbose=True, fail=True)
        report.add(self.TooMuchData(remove_unused), verbose=True)
        if reindex:
            report.add(self.Reindex(), verbose=True)
        return report.get()
    
if __name__=="__main__":
    exit("Don't run this file")