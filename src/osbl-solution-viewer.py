#! /usr/bin/env python3
import sys
import os

if __name__ != "__main__":
    exit('This script should only be executed directly')
else:
    sys.path.append(os.path.join(os.path.dirname(__file__),'ortec','scientific','benchmarks'))
    from loadbuilding import SolutionViewer
    SolutionViewer.main()