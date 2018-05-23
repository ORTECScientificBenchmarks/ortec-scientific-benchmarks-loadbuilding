from ..Requirements import BaseConstraint, ExistenceRequirement, PropositionalRequirement
from ..NgoiMatrix import NgoiMatrix
from ..utils import key, Orientation
from ...solution.ThreeDplacement import ThreeDplacement

class ReadableItemLabelConstraint(BaseConstraint):
    name = "readable_item_labels"
    itemkindRequirements = [ExistenceRequirement("label", "L", str),
                            PropositionalRequirement("label", lambda x: x in ['L','W','H','l','w','h'], "label must be one of L,W,H,l,w,h")]

    class Dummy(ThreeDplacement):
        def __init__(self):
            super(ReadableItemLabelConstraint.Dummy, self).__init__()
        @staticmethod
        def TypeString():
            return "label of item"

    def GetDummies(loadingspace):
        dummies = []
        for placement in loadingspace.placements:
            if hasattr(placement, "label"):
                dummy = ReadableItemLabelConstraint.Dummy()
                dummy.__dict__ = {x: placement.__dict__[x] for x in placement.__dict__ if x not in ['position', 'boundingBox']}
                dummy.position    = list(placement.position)
                dummy.boundingBox = list(placement.boundingBox)
                global_label = Orientation.ApplyToSide(Orientation.GetFromAlias(dummy.orientation), dummy.label)
                if global_label == 'l':
                    dummy.boundingBox[0] = dummy.position[0]
                    dummy.position[0] = 0
                elif global_label == 'w':
                    dummy.boundingBox[1] = dummy.position[1]
                    dummy.position[1] = 0
                elif global_label == 'h':
                    dummy.boundingBox[2] = dummy.position[2]
                    dummy.position[2] = 0
                elif global_label == 'L':
                    dummy.position[0] = dummy.position[0] + dummy.boundingBox[0]
                    dummy.boundingBox[0] = loadingspace.boundingBox[0] - dummy.position[0]
                elif global_label == 'W':
                    dummy.position[1] = dummy.position[1] + dummy.boundingBox[1]
                    dummy.boundingBox[1] = loadingspace.boundingBox[1] - dummy.position[1]
                elif global_label == 'H':
                    dummy.position[2] = dummy.position[2] + dummy.boundingBox[2]
                    dummy.boundingBox[2] = loadingspace.boundingBox[2] - dummy.position[2]
                dummies.append((dummy, global_label))
        return dummies

    def Validate(threeDsolution):
        valid, errors = True, [""]
        for pallet in threeDsolution.pallets:
            ngoi = NgoiMatrix(*pallet.loadingspace.boundingBox)
            # Add dummy objects to each placement that represent the free space required for label visibility
            dummies_labels = ReadableItemLabelConstraint.GetDummies(pallet.loadingspace)
            dummies, _ = zip(*dummies_labels)
            dummies = list(dummies)
            for dummy,label in dummies_labels:
                if label.upper() == 'H':
                    valid = False
                    errors.append("Label of item with id " + str(dummy.id) + " was facing along H-direction <- VIOLATION")
            for placement in sorted(pallet.loadingspace.placements + dummies, key=lambda x: x.position[2]):
                ngoi.addCuboid(placement)
            for pair in ngoi.overlaps():
                pair.sort(key=key("id"))
                if pair[0].TypeString() != "label of item" or pair[1].TypeString() != "label of item":
                    valid = False
                    errors.append(pair[0].TypeString().capitalize() + " with id " + str(pair[0].id) + " overlaps with " + pair[1].TypeString().capitalize() + " with id " + str(pair[1].id) + " <- VIOLATION")
            errors += ngoi.overlap_report
        return valid, ("All" if valid else "Not all") + " item labels were visible" + ("." if valid else ":" + "\n\t- ".join(set(errors)))
        
if __name__=="__main__":
    exit("Don't run this file")