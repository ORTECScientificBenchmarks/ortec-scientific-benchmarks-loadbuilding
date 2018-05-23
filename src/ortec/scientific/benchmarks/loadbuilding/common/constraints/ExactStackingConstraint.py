from ..Requirements import BaseConstraint
from ..utils import flatten

class ExactStackingConstraint(BaseConstraint):
    name = "exact_stacking"
    
    def Validate(threeDsolution):
        valid, errors = True, [""]
        for container in threeDsolution.containers:
            for loadingspace in container.loadingspaces:
                placement_support = {}
                placement_ids_above = {}
                for placement in loadingspace.placements:
                    placement_support[placement.id] = True
                    placement_ids_above[placement.id] = set()
                for ngoicell in flatten(loadingspace.ngoi.ngoi):
                    _, stacking = ngoicell
                    current_height = 0
                    current_item = None
                    for element in stacking:
                        h,s = element[0], element[1]
                        if current_item is None:
                            if current_height != h:
                                placement_support[s.id] = False
                        else:
                            if current_height+current_item.boundingBox[2] != h:
                                placement_support[s.id] = False
                            else:
                                placement_ids_above[current_item.id].add(s.id)
                        current_height = h
                        current_item   = s
                    placement_ids_above[s.id].add(None)
                for k in placement_support:
                    if not placement_support[k]:
                        valid = False
                        errors.append("Placement with id " + str(k) + " is not properly supported <- VIOLATION")
                for k in placement_ids_above:
                    if len(placement_ids_above[k]) != 1:
                        valid = False
                        errors.append("Placement with id " + str(k) + " is not exactly covered from above <- VIOLATION")
        return valid, ("All" if valid else "Not all") + " placements were exactly stacked" + ("." if valid else ":" + "\n\t- ".join(errors))

if __name__=="__main__":
    exit("Don't run this file")