import argparse
import os
import sys
from . import LoadbuildInstance
from .common import Requirements
    
class ApplicableConstraintsObjectives(object):
    pass

class HidePrint(object):
    def __enter__(self):
        self._stdout_ = sys.stdout
        sys.stdout = None
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._stdout_

def main(args=None):
    parser = argparse.ArgumentParser(description='Report applicable constraints and objectives')
    parser.add_argument('--input', '-I', metavar='INPUT_FILE', required=True,
                        help='The input file')
    parser.add_argument('--type', '-t', metavar='TYPE',  choices=['json', 'yaml', 'xml'],
                        help='The type of the input file')
    args = parser.parse_args(args)

    if args.type is None:
        filename = args.input
        _, file_extension = os.path.splitext(filename)
        if file_extension in ['.json', '.xml', '.yaml']:
            args.type = file_extension[1:]

    converter = LoadbuildInstance.LoadbuildInstance(args.input,args.type,'','')
    b,e = converter.lbInstance.IsValid()
    if not b:
        raise Exception(e)
    with HidePrint():
        b,e = converter.lbInstance.IsDataComplete()
        if not b:
            raise Exception(e)
    
    applicable = ["The following objective(s) can be applied given the data from the instance '%s':" % (converter.lbInstance.description.InstanceName())]
    not_applicable = ["The following objective(s) can not be applied given the data from the instance '%s':" % (converter.lbInstance.description.InstanceName())]
    for o in sorted(Requirements.BaseRequirement.OBJECTIVE_LIST, key=lambda o: o.name):
        b,e = o.TestDataRequirements(converter.lbInstance)
        if b:
            applicable.append(o.name)
        else:
            not_applicable.append(o.name)
    if len(applicable) > 1:
        print("\n\t- ".join(applicable))
    if len(not_applicable) > 1:
        print("\n\t- ".join(not_applicable))
    applicable = ["The following constraint(s) can be applied given the data from the instance '%s':" % (converter.lbInstance.description.InstanceName())]
    not_applicable = ["The following constraint(s) can not be applied given the data from the instance '%s':" % (converter.lbInstance.description.InstanceName())]
    for c in sorted(Requirements.BaseRequirement.CONSTRAINT_LIST, key=lambda c: c.name):
        b,e = o.TestDataRequirements(converter.lbInstance)
        if b:
            applicable.append(c.name)
        else:
            not_applicable.append(c.name)
    if len(applicable) > 1:
        print("\n\t- ".join(applicable))
    if len(not_applicable) > 1:
        print("\n\t- ".join(not_applicable))
        
if __name__=="__main__":
    exit("Don't run this file")