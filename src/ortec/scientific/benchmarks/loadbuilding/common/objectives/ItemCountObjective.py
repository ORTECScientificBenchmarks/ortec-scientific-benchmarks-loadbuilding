from ..Requirements import BaseObjective

# MAXIMIZE
class ItemCountObjective(BaseObjective):
    name = "item_count"
    def Evaluate(threeDsolution):
        return -sum([1 for placement in threeDsolution.GetAllPlacements() if placement.position != placement.UNPLACED and placement.itemid is not None])

if __name__=="__main__":
    exit("Don't run this file")