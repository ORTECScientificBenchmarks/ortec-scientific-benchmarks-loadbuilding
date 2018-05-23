import argparse
import os

class LoadbuildInstance(object):
    def _jsonToLB_(self,jsonInstanceLocation):
        from .instance.read.JSONtoThreeDinstance import JSONtoThreeDinstance
        jsonToLB = JSONtoThreeDinstance(jsonInstanceLocation)
        self.lbInstance = jsonToLB.CreateThreeDinstance()
        
    def _ortecToLB_(self,ortecInstanceLocation):
        from .instance.read.CLBStoThreeDinstance import CLBStoThreeDinstance
        clbsToLB = CLBStoThreeDinstance(ortecInstanceLocation)
        self.lbInstance = clbsToLB.CreateThreeDinstance()
    
    def _xmlToLB_(self,xmlInstanceLocation):
        from .instance.read.XMLtoThreeDinstance import XMLtoThreeDinstance
        xmlToLB = XMLtoThreeDinstance(xmlInstanceLocation)
        self.lbInstance = xmlToLB.CreateThreeDinstance()

    def _yamlToLB_(self,yamlInstanceLocation):
        from .instance.read.YAMLtoThreeDinstance import YAMLtoThreeDinstance
        yamlToLB = YAMLtoThreeDinstance(yamlInstanceLocation)
        self.lbInstance = yamlToLB.CreateThreeDinstance()
        
    def _LBtoJSON_(self,outputfile):
        from .instance.write.ThreeDinstanceToJSON import ThreeDinstanceToJSON
        lbToJSON = ThreeDinstanceToJSON(self.lbInstance)
        lbToJSON.WriteInstance(outputfile)
        
    def _LBtoXML_(self,outputfile):
        from .instance.write.ThreeDinstanceToXML import ThreeDinstanceToXML
        lbToXML = ThreeDinstanceToXML(self.lbInstance)
        lbToXML.WriteInstance(outputfile)
        
    def _LBtoYAML_(self,outputfile):
        from .instance.write.ThreeDinstanceToYAML import ThreeDinstanceToYAML
        lbToYAML = ThreeDinstanceToYAML(self.lbInstance)
        lbToYAML.WriteInstance(outputfile)

    def _CreateInstance_(self,outputfile,outputType):
        if outputType == 'json':
            self._LBtoJSON_(outputfile)
        elif outputType == 'yaml':
            self._LBtoYAML_(outputfile)
        elif outputType == 'xml':
            self._LBtoXML_(outputfile)
        else:
            raise Exception("Unknown output type: " + outputType)
    
    def __init__(self,filename,filetype,setname,name):
        if filetype == 'ortec':
            self._ortecToLB_(filename)
        elif filetype == 'json':
            self._jsonToLB_(filename)
        elif filetype == 'yaml':
            self._yamlToLB_(filename)
        elif filetype == 'xml':
            self._xmlToLB_(filename)
        else:
            raise Exception("Unknown input file type: " + filetype)
        if setname:
            self.OverwriteSetname(setname)
        if name:
            self.OverwriteInstancename(name)

    def CreateInstance(self,outputfilebasename,outputtypes):
        for t in outputtypes:
            outputfile = outputfilebasename + '.' + t
            self._CreateInstance_(outputfile,t)
            
    def OverwriteSetname(self,setname):
        self.lbInstance.description.setname = setname
    
    def OverwriteInstancename(self,instancename):
        self.lbInstance.description.name = instancename

def main(args=None):
    parser = argparse.ArgumentParser(description='Convert loadbuilding instances')
    parser.add_argument('--input', '-I', metavar='INPUT_FILE', required=True, help='The input file')
    parser.add_argument('--type', '-t', metavar='TYPE', choices=['json', 'yaml', 'xml', 'ortec'], help='The type of the input file, choose one of: json, xml, yaml')
    parser.add_argument('--output', '-O', metavar='OUTPUT_FILE', help='The output file basename, extension is set by output type')
    parser.add_argument('--xml', '-X', action='store_true', help='Create xml file')
    parser.add_argument('--yaml', '-Y', action='store_true', help='Create yaml file')
    parser.add_argument('--json', '-J', action='store_true', help='Create json file')
    parser.add_argument('--setname', help='Overwrite the set name')
    parser.add_argument('--instancename', help='Overwrite the instance name')
    parser.add_argument('--reindex', '-R', action='store_true', help='Reindex ids to lowest possible')
    parser.add_argument('--remove_unused', '-U', action='store_true', help='Remove unused optional fields')
    args = parser.parse_args(args)

    if args.type is None:
        filename = args.input
        _, file_extension = os.path.splitext(filename)
        if file_extension in ['.json', '.xml', '.yaml']:
            args.type = file_extension[1:]
    if (args.json or args.yaml or args.xml) and args.output is None:
        if args.setname is None or args.instancename is None:
            exit('Could not deduce output filename setname or instancename is not given')
        else:
            args.output = args.setname + '_' + args.instancename
    
    converter = LoadbuildInstance(args.input,args.type,args.setname,args.instancename)
    converter.lbInstance.AllChecks(reindex=args.reindex, remove_unused=args.remove_unused)

    outputTypes = list()
    if args.xml:
        outputTypes.append('xml')
    if args.json:
        outputTypes.append('json')
    if args.yaml:
        outputTypes.append('yaml')
    converter.CreateInstance(args.output,outputTypes)
    if not outputTypes:
        print("Instance '%s' is valid" % (converter.lbInstance.description.InstanceName()))

if __name__=="__main__":
    exit("Don't run this file")