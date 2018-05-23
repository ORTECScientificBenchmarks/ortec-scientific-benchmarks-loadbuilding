from ..common.utils import indent

class ThreeDdescription(object):
    def __init__(self):
        self.setname = None
        self.name    = None
        
    def IsValid(self):
        errors = [""]
        
        if self.setname is None:
            errors.append("Set name undefined")
        elif not isinstance(self.setname,str):
            errors.append("Set name should be string")
        elif not self.setname:
            errors.append("Set name should be nonempty")
            
        if self.name is None:
            errors.append("Instance name undefined")
        elif not isinstance(self.name,str):
            errors.append("Instance name should be string")
        elif not self.name:
            errors.append("Instance name should be nonempty")
        if len(errors)>1:
            return False, "Description invalid:" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "description"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)
        
    def InstanceName(self):
        return '%s %s' % (self.setname,self.name) 
        
if __name__=="__main__":
    exit("Don't run this file")
