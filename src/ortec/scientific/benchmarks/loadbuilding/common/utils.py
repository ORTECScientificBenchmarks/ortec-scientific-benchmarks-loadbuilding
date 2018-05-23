def prod(_list):
    res = 1
    for element in _list:
        res *= element
    return res

def mean(_list):
    res = 0
    for element in _list:
        res += element
    return res/len(_list)

def bool_cast(s):
    if s.lower() == "false":
        return False
    return True

def indent(string):
    return "\n\t".join(string.split("\n"))

def flatten(list_of_lists):
    return [j for i in list_of_lists for j in i]

def key(attribute, default=-float('infinity')):
    return (lambda x: getattr(x, attribute) if hasattr(x, attribute) and getattr(x, attribute) is not None and (isinstance(getattr(x, attribute), float) or isinstance(getattr(x, attribute), int)) else default)

def combine(lambdas):
    return (lambda x: [lambd(x) for lambd in lambdas])

def testListOnId(listOfObjects):
    allIds = [x.id for x in listOfObjects if hasattr(x, "id") and isinstance(x.id, int)]
    sortedIds = sorted(set(allIds))
    return sorted(allIds) == sortedIds

def testListOnName(listOfObjects):
    allNames = [x.name for x in listOfObjects if hasattr(x, "name") and isinstance(x.name, str)]
    sortedNames = sorted(set(allNames))
    return sorted(allNames) == sortedNames

def checkDuplicateIds(x):
    if testListOnId(x):
        return True, ""
    return False, "Duplicate " + x[0].TypeString() + " ids <- VIOLATION"
    
def checkDuplicateNames(x):
    if testListOnName(x):
        return True, ""
    return False, "Duplicate " + x[0].TypeString() + " names <- VIOLATION"

class Report:
    def __init__(self):
        self.valid  = True
        self.report = list()
        
    def add(self, tup, verbose=False, fail=False, title=True):
        if not isinstance(tup, tuple) or len(tup) != 2 or not isinstance(tup[0], bool) or not isinstance(tup[1], str):
            raise Exception("Expected a (bool,str)-tuple in report")
        valid  = tup[0]
        report = tup[1]
        if title:
            report = report[:1].upper() + report[1:]
        self.valid = self.valid and valid
        if report:
            self.report.append(report)
        if not valid and fail:
            raise Exception(report)
        if report and verbose:
            print(report)
            
    def get(self):
        return self.valid, "\n".join(self.report)

class Orientation:
    LWH = set(['LWH', 'Lwh', 'lWh', 'lwH'])
    WLH = set(['WLh', 'WlH', 'wLH', 'wlh'])
    LHW = set(['LHw', 'LhW', 'lHW', 'lhw'])
    HLW = set(['HLW', 'Hlw', 'hLw', 'hlW'])
    WHL = set(['WHL', 'Whl', 'wHl', 'whL'])
    HWL = set(['HWl', 'HwL', 'hWL', 'hwl'])

    ALL          = LWH | WLH | LHW | HLW | WHL | HWL
    L_ON_GROUND  = LWH | WLH | LHW | HLW
    THIS_SIDE_UP = set(['LWH', 'lwH', 'WlH', 'wLH'])

    @staticmethod
    def GetFromAlias(alias):
        if alias == 'LHW':
            return 'LhW'
        elif alias == 'WLH':
            return 'WlH'
        elif alias == 'HWL':
            return 'HwL'
        else:
            return alias

    @staticmethod
    def IsValid(orientation):
        if not isinstance(orientation, str) or set(orientation.upper()) != {'L','W','H'}:
            return False
        perm_axes = 1 if orientation[orientation.upper().find('L')-1].upper() == 'H' else -1
        flip_axes = prod([1 if o.isupper() else -1 for o in orientation])
        return perm_axes * flip_axes > 0

    @staticmethod
    def ApplyToSide(orientation, side):
        index  = orientation.upper().find(side.upper())
        symbol = "LWH"[index]
        return symbol.upper() if (orientation[index].isupper() == side.isupper()) else symbol.lower()
        
if __name__=="__main__":
    exit("Don't run this file")