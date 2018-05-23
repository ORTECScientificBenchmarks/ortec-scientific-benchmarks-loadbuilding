from ..Requirements import BaseObjective

# MINIMIZE
class ContainerCountObjective(BaseObjective):
    name = "container_count"
    def Evaluate(threeDsolution):
        return len(threeDsolution.containers)
        
if __name__=="__main__":
    exit("Don't run this file")