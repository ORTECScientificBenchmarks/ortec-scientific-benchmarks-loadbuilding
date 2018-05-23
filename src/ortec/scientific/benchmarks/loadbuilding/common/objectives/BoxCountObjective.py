from ..Requirements import BaseObjective

# MINIMIZE
class BoxCountObjective(BaseObjective):
    name = "box_count"
    def Evaluate(threeDsolution):
        return len(threeDsolution.boxes)
        
if __name__=="__main__":
    exit("Don't run this file")