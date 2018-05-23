import os
import argparse
from . import LoadbuildInstance

class LoadbuildSolution(object):
    def _jsonToSol_(self,lbInstance,jsonSolutionLocation):
        from .solution.read.JSONtoThreeDsolution import JSONtoThreeDsolution
        jsonToSol = JSONtoThreeDsolution(jsonSolutionLocation)
        self.lbSolution = jsonToSol.CreateThreeDsolution(lbInstance)

    def _yamlToSol_(self,lbInstance,yamlSolutionLocation):
        from .solution.read.YAMLtoThreeDsolution import YAMLtoThreeDsolution
        yamlToSol = YAMLtoThreeDsolution(yamlSolutionLocation)
        self.lbSolution = yamlToSol.CreateThreeDsolution(lbInstance)

    def _xmlToSol_(self,lbInstance,xmlSolutionLocation):
        from .solution.read.XMLtoThreeDsolution import XMLtoThreeDsolution
        xmlToSol = XMLtoThreeDsolution(xmlSolutionLocation)
        self.lbSolution = xmlToSol.CreateThreeDsolution(lbInstance)

    def _solToJSON_(self,outputfile):
        from .solution.write.ThreeDsolutionToJSON import ThreeDsolutionToJSON
        solToJSON = ThreeDsolutionToJSON(self.lbSolution)
        solToJSON.WriteSolution(outputfile)

    def _solToYAML_(self,outputfile):
        from .solution.write.ThreeDsolutionToYAML import ThreeDsolutionToYAML
        solToYAML = ThreeDsolutionToYAML(self.lbSolution)
        solToYAML.WriteSolution(outputfile)
        
    def _solToXML_(self,outputfile):
        from .solution.write.ThreeDsolutionToXML import ThreeDsolutionToXML
        solToXML = ThreeDsolutionToXML(self.lbSolution)
        solToXML.WriteSolution(outputfile)

    def _CreateSolution_(self,outputfile,outputType):
        if outputType == 'json':
            self._solToJSON_(outputfile)
        elif outputType == 'yaml':
            self._solToYAML_(outputfile)
        elif outputType == 'xml':
            self._solToXML_(outputfile)
        else:
            raise Exception("Unknown output type: " + outputType)
        
    def __init__(self,instancename,instancetype,solutionname,solutiontype,setname,name):
        instance             = LoadbuildInstance.LoadbuildInstance(instancename, instancetype, "", "")
        instance_in_solution = LoadbuildInstance.LoadbuildInstance(solutionname, solutiontype, "", "")
        instance.lbInstance.AllChecks()
        
        if solutiontype == 'json':
            self._jsonToSol_(instance.lbInstance, solutionname)
        elif solutiontype == 'yaml':
            self._yamlToSol_(instance.lbInstance, solutionname)
        elif solutiontype == 'xml':
            self._xmlToSol_(instance.lbInstance, solutionname)
        else:
            raise Exception("Unknown solution file type: " + solutiontype)
        if instance.lbInstance != instance_in_solution.lbInstance and\
          not (instance_in_solution.lbInstance.constraints     == [] and\
               instance_in_solution.lbInstance.objectives      == [] and\
               instance_in_solution.lbInstance.containerkinds  == [] and\
               instance_in_solution.lbInstance.itemkinds       == []):
            raise Exception("Either specify the entire instance in the solution file, or no instance at all")
        if setname:
            self.OverwriteSetname(setname)
        if name:
            self.OverwriteInstancename(name)
        self.lbSolution.DecorateSolution()

    def CreateSolution(self,outputfilebasename,outputtypes):
        for t in outputtypes:
            outputfile = outputfilebasename + '.' + t
            self._CreateSolution_(outputfile,t)

    def OverwriteSetname(self,setname):
        self.lbSolution.description.setname = setname
        self.lbSolution.threeDinstance.description.setname = setname
    
    def OverwriteInstancename(self,instancename):
        self.lbSolution.description.name = instancename
        self.lbSolution.threeDinstance.description.name = instancename

def main(args=None):
    parser = argparse.ArgumentParser(description='Convert loadbuilding solutions')
    parser.add_argument('--instance',     '-I',  metavar='INPUT_FILE',    required=True,                   help='The instance file')
    parser.add_argument('--instancetype', '-IT', metavar='INSTANCE_TYPE', choices=['json', 'yaml', 'xml'], help='The type of the instance file')
    parser.add_argument('--solution',     '-S',  metavar='SOLUTION_FILE', required=True,                   help='The solution file')
    parser.add_argument('--solutiontype', '-ST', metavar='SOLUTION_TYPE', choices=['json', 'yaml', 'xml'], help='The type of the solution file')
    parser.add_argument('--output', '-O', metavar='OUTPUT_FILE', help='The output file basename, extension is set by output type')
    parser.add_argument('--xml', '-X', action='store_true',  help='Create xml file')
    parser.add_argument('--yaml', '-Y', action='store_true', help='Create yaml file')
    parser.add_argument('--json', '-J', action='store_true', help='Create json file')
    parser.add_argument('--setname', help='Overwrite the set name')
    parser.add_argument('--instancename', help='Overwrite the instance name')
    args = parser.parse_args(args)

    if args.instancetype is None:
        filename = args.instance
        _, file_extension = os.path.splitext(filename)
        if file_extension in ['.json', '.xml', '.yaml']:
            args.instancetype = file_extension[1:]
    if args.solutiontype is None:
        filename = args.solution
        _, file_extension = os.path.splitext(filename)
        if file_extension in ['.json', '.xml', '.yaml']:
            args.solutiontype = file_extension[1:]
    if (args.json or args.yaml or args.xml) and args.output is None:
        if args.setname is None or args.instancename is None:
            exit('Could not deduce output filename setname or instancename is not given')
        else:
            args.output = args.setname + '_' + args.instancename

    converter = LoadbuildSolution(args.instance,args.instancetype,args.solution,args.solutiontype,args.setname,args.instancename)
    
    outputTypes = list()
    if args.xml:
        outputTypes.append('xml')
    if args.json:
        outputTypes.append('json')
    if args.yaml:
        outputTypes.append('yaml')
    converter.CreateSolution(args.output,outputTypes)
    if not outputTypes:
        converter.lbSolution.PrintResults()

if __name__=="__main__":
    exit("Don't run this file")