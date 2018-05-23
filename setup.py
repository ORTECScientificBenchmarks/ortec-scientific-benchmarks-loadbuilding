from setuptools import setup

setup   (test_suite = 'nose.collector'
        ,tests_require = ['nose','coverage']
        ,entry_points = {   'console_scripts': 
                                [ 'osbl-instance = ortec.scientific.benchmarks.loadbuilding.LoadbuildInstance:main'
                                , 'osbl-solution = ortec.scientific.benchmarks.loadbuilding.LoadbuildSolution:main'
                                , 'osbl-solution-viewer = ortec.scientific.benchmarks.loadbuilding.SolutionViewer:main'
                                , 'osbl-find-constraints-objectives = ortec.scientific.benchmarks.loadbuilding.ApplicableConstraintsObjectives:main'
                                ]
                        }
        )