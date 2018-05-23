import unittest, io, sys
from ortec.scientific.benchmarks.loadbuilding.common.utils import prod, mean, bool_cast, indent, flatten, key, combine, testListOnId, testListOnName, checkDuplicateIds, checkDuplicateNames, Report, Orientation

class TestMiscellaneous(unittest.TestCase):
    def test_prod(self):
        self.assertEqual(prod([1]), 1)
        self.assertEqual(prod([1, 1]), 1)
        self.assertEqual(prod([1, 1, 1]), 1)
        self.assertEqual(prod([-1, 0, 1]), 0)
        self.assertEqual(prod([0, 1, 2]), 0)
        self.assertEqual(prod([0, 5, 10]), 0)
        self.assertEqual(prod([10, 20, 30]), 6000)
    
    def test_mean(self):
        self.assertEqual(mean([1]), 1)
        self.assertEqual(mean([1, 1]), 1)
        self.assertEqual(mean([1, 1, 1]), 1)
        self.assertEqual(mean([-1, 0, 1]), 0)
        self.assertEqual(mean([0, 1, 2]), 1)
        self.assertEqual(mean([0, 5, 10]), 5)
        self.assertEqual(mean([10, 20, 30]), 20)
    
    def test_boolcast(self):
        self.assertEqual(bool_cast("False"), False)
        self.assertEqual(bool_cast("false"), False)
        self.assertEqual(bool_cast("True"), True)
        self.assertEqual(bool_cast("true"), True)

    def test_indent(self):
        self.assertEqual(indent(""), "")
        self.assertEqual(indent("Noindent"), "Noindent")
        self.assertEqual(indent("Indent\nthis!"), "Indent\n\tthis!")

    def test_utils_flatten(self):
        for n in range(10):
            self.assertEqual(flatten([[i] for i in range(n)]), list(range(n)))
            self.assertEqual(flatten(n*[list(range(n))]),    n*list(range(n)))

    def test_key(self):
        class A:
            def __init__(self,id):
                self.id = id
        self.assertEqual(key("id")(0), -float('infinity'))
        self.assertEqual(key("id")("<placement id='1' itemid='1'>"), -float('infinity'))
        self.assertEqual(key("id")(A(0)), 0)
        self.assertEqual(key("id")(A(1)), 1)
        self.assertEqual(key("id")(A(2)), 2)
        self.assertEqual(key("id")(A("test")), -float('infinity'))
        self.assertEqual(key("id")(A(A(0))),   -float('infinity'))

    def test_combine(self):
        self.assertEqual(combine([sum,len])([]), [0,0])
        self.assertEqual(combine([sum,len])([1]), [1,1])
        self.assertEqual(combine([sum,len])([1,2]), [3,2])
        self.assertEqual(combine([sum,len])([1,2,3]), [6,3])
        self.assertEqual(combine([type,lambda x: x*x])(1), [int,1])
        self.assertEqual(combine([type,lambda x: x*x])(10), [int,100])
        self.assertEqual(combine([type,lambda x: x*x])(100), [int,10000])

    def test_utils_testlistonid(self):
        class A:
            def __init__(self,id):
                self.id = id
        for n in range(10):
            ids = [A(id) for id in range(n)]
            self.assertTrue(testListOnId(ids))
            if ids:
                ids.append(ids[n//2])
                self.assertFalse(testListOnId(ids))

    def test_utils_testlistonname(self):
        class A:
            def __init__(self,name):
                self.name = name
        for n in range(10):
            names = [A(name) for name in [i*"abc" for i in range(n)]]
            self.assertTrue(testListOnName(names))
            if names:
                names.append(names[n//2])
                self.assertFalse(testListOnName(names))

    def test_utils_checkduplicateids(self):
        class A:
            def __init__(self,id):
                self.id = id
            @staticmethod
            def TypeString():
                return "A"
        for n in range(10):
            ids = [A(id) for id in range(n)]
            self.assertEqual(checkDuplicateIds(ids), (True, ""))
            if ids:
                ids.append(ids[n//2])
                self.assertEqual(checkDuplicateIds(ids), (False, "Duplicate A ids <- VIOLATION"))

    def test_utils_checkduplicatenames(self):
        class A:
            def __init__(self,name):
                self.name = name
            @staticmethod
            def TypeString():
                return "A"
        for n in range(10):
            names = [A(name) for name in [i*"abc" for i in range(n)]]
            self.assertEqual(checkDuplicateNames(names), (True, ""))
            if names:
                names.append(names[n//2])
                self.assertEqual(checkDuplicateNames(names), (False, "Duplicate A names <- VIOLATION"))

class TestReport(unittest.TestCase):
    def test_utils_report(self):
        report = Report()
        self.assertEqual(report.get(), (True, ""))
        self.assertRaises(Exception, report.add, None)
        self.assertRaises(Exception, report.add, True)
        self.assertRaises(Exception, report.add, False)
        self.assertRaises(Exception, report.add, "")
        report.add((True, ""))
        self.assertEqual(report.get(), (True,""))
        report.add((False, "Error #1 happened"))
        self.assertEqual(report.get(), (False, "Error #1 happened"))
        report.add((False, "Error #2 happened"))
        self.assertEqual(report.get(), (False, "Error #1 happened\nError #2 happened"))
        self.assertRaises(Exception, report.add, (False, "Fail"), False, True)
        
        temp_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        report.add((True, "Time to be verbose"), verbose=True)
        self.assertEqual(captured_output.getvalue(), "Time to be verbose\n")
        sys.stdout = temp_stdout
        
class TestOrientation(unittest.TestCase):
    def test_utils_orientation_isvalid(self):
        self.assertFalse(Orientation.IsValid(None))
        self.assertFalse(Orientation.IsValid(""))
        for c in ['l', 'L', 'w', 'W', 'h', 'H']:
            self.assertFalse(Orientation.IsValid(3*c))
        
        for l_index in range(3):
            for w_index in range(3):
                if l_index == w_index: continue
                for h_index in range(3):
                    if l_index == h_index or w_index == h_index: continue
                    for l_cap in [False, True]:
                        for w_cap in [False, True]:
                            for h_cap in [False, True]:
                                orientation = 3*[""]
                                orientation[l_index] = "L" if l_cap else "l"
                                orientation[w_index] = "W" if w_cap else "w"
                                orientation[h_index] = "H" if h_cap else "h"
                                orientation = "".join(orientation)
                                if orientation in Orientation.ALL:
                                    self.assertTrue(Orientation.IsValid(orientation))
                                else:
                                    self.assertFalse(Orientation.IsValid(orientation))
                                    
    def test_utils_orientation_getfromalias(self):
        self.assertEqual(Orientation.GetFromAlias("LWH"), "LWH")
        self.assertEqual(Orientation.GetFromAlias("LHW"), "LhW")
        self.assertEqual(Orientation.GetFromAlias("WLH"), "WlH")
        self.assertEqual(Orientation.GetFromAlias("WHL"), "WHL")
        self.assertEqual(Orientation.GetFromAlias("HLW"), "HLW")
        self.assertEqual(Orientation.GetFromAlias("HWL"), "HwL")
        
    def test_utils_orientation_applytoside(self):
        result = {'LWH': {'L': 'L', 'l': 'l', 'W': 'W', 'w': 'w', 'H': 'H', 'h': 'h'},
                  'Lwh': {'L': 'L', 'l': 'l', 'W': 'w', 'w': 'W', 'H': 'h', 'h': 'H'},
                  'lWh': {'L': 'l', 'l': 'L', 'W': 'W', 'w': 'w', 'H': 'h', 'h': 'H'},
                  'lwH': {'L': 'l', 'l': 'L', 'W': 'w', 'w': 'W', 'H': 'H', 'h': 'h'},
                  'LHw': {'L': 'L', 'l': 'l', 'W': 'h', 'w': 'H', 'H': 'W', 'h': 'w'},
                  'LhW': {'L': 'L', 'l': 'l', 'W': 'H', 'w': 'h', 'H': 'w', 'h': 'W'},
                  'lHW': {'L': 'l', 'l': 'L', 'W': 'H', 'w': 'h', 'H': 'W', 'h': 'w'},
                  'lhw': {'L': 'l', 'l': 'L', 'W': 'h', 'w': 'H', 'H': 'w', 'h': 'W'},
                  'WHL': {'L': 'H', 'l': 'h', 'W': 'L', 'w': 'l', 'H': 'W', 'h': 'w'},
                  'Whl': {'L': 'h', 'l': 'H', 'W': 'L', 'w': 'l', 'H': 'w', 'h': 'W'},
                  'wHl': {'L': 'h', 'l': 'H', 'W': 'l', 'w': 'L', 'H': 'W', 'h': 'w'},
                  'whL': {'L': 'H', 'l': 'h', 'W': 'l', 'w': 'L', 'H': 'w', 'h': 'W'},
                  'WLh': {'L': 'W', 'l': 'w', 'W': 'L', 'w': 'l', 'H': 'h', 'h': 'H'},
                  'WlH': {'L': 'w', 'l': 'W', 'W': 'L', 'w': 'l', 'H': 'H', 'h': 'h'},
                  'wLH': {'L': 'W', 'l': 'w', 'W': 'l', 'w': 'L', 'H': 'H', 'h': 'h'},
                  'wlh': {'L': 'w', 'l': 'W', 'W': 'l', 'w': 'L', 'H': 'h', 'h': 'H'},
                  'HLW': {'L': 'W', 'l': 'w', 'W': 'H', 'w': 'h', 'H': 'L', 'h': 'l'},
                  'Hlw': {'L': 'w', 'l': 'W', 'W': 'h', 'w': 'H', 'H': 'L', 'h': 'l'},
                  'hLw': {'L': 'W', 'l': 'w', 'W': 'h', 'w': 'H', 'H': 'l', 'h': 'L'},
                  'hlW': {'L': 'w', 'l': 'W', 'W': 'H', 'w': 'h', 'H': 'l', 'h': 'L'},
                  'HWl': {'L': 'h', 'l': 'H', 'W': 'W', 'w': 'w', 'H': 'L', 'h': 'l'},
                  'HwL': {'L': 'H', 'l': 'h', 'W': 'w', 'w': 'W', 'H': 'L', 'h': 'l'},
                  'hWL': {'L': 'H', 'l': 'h', 'W': 'W', 'w': 'w', 'H': 'l', 'h': 'L'},
                  'hwl': {'L': 'h', 'l': 'H', 'W': 'w', 'w': 'W', 'H': 'l', 'h': 'L'}}
        for orientation in Orientation.ALL:
            for side in ['l', 'L', 'w', 'W', 'h', 'H']:
                self.assertEqual(result[orientation][side], Orientation.ApplyToSide(orientation, side))

TestCase = unittest.TestSuite()
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMiscellaneous))
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReport))
TestCase.addTest(unittest.TestLoader().loadTestsFromTestCase(TestOrientation))
