from ..Requirements import BaseObjective
from ..utils import prod, mean

def fillRates(threeDsolution):
    fill_rates = list()
    for container in threeDsolution.containers:
        container_volume = sum([prod(loadingspace.boundingBox) for loadingspace in container.loadingspaces])
        fill_volume = sum([sum([prod(placement.boundingBox) for placement in loadingspace.placements]) for loadingspace in container.loadingspaces])
        fill_rates.append(fill_volume/container_volume)
    return fill_rates

# Average container fill rate (MAXIMIZE)
class AverageFillRateObjective(BaseObjective):
    name = "average_fill_rate"
    def Evaluate(threeDsolution):
        return -mean(fillRates(threeDsolution))

# Worst container fill rate (MAXIMIZE)
class WorstFillRateObjective(BaseObjective):
    name = "worst_fill_rate"
    def Evaluate(threeDsolution):
        return -min(fillRates(threeDsolution))
        
if __name__=="__main__":
    exit("Don't run this file")