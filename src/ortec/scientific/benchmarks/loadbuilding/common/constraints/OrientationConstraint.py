from ..Requirements import BaseConstraint
from ..utils import Orientation

class OrientationConstraint(BaseConstraint):
    name = "orientation"
    
    def Validate(threeDsolution):
        valid, errors = True, [""]
        for container in sorted(threeDsolution.containers, key=lambda x: x.id):
            for loadingspace in sorted(container.loadingspaces, key=lambda x: x.id):
                for placement in sorted(loadingspace.placements, key=lambda x: [x.type, x.id]):
                    rep = placement.type.capitalize() + " with id " + str(placement.id) + " has orientation " + placement.orientation + ("" if placement.orientation in placement.orientations else " not") + " in " + str(placement.orientations)
                    if placement.orientation not in placement.orientations:
                        placement.correct = False
                        valid = False
                        rep += " <- VIOLATION"
                    errors.append(rep)
        return valid, ("All" if valid else "Not all") + " placements had valid orientations" + ("." if valid else ":" + "\n\t- ".join(errors))

if __name__=="__main__":
    exit("Don't run this file")