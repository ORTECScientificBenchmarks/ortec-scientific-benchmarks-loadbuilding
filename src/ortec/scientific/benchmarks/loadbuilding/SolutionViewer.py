def colorcode(r,g,b,a):
    return '#%02x%02x%02x%02x' % r,g,b,a

import vpython
import os
import argparse
from distutils.version import LooseVersion
from . import LoadbuildSolution

def placement_to_box(placement):
    x0,y0,z0 = placement[0]
    x1,y1,z1 = placement[1]
    xc,yc,zc = (x0+x1)/2, (y0+y1)/2, (z0+z1)/2
    l,w,h    = abs(x1-x0), abs(y1-y0), abs(z1-z0)
    return ((xc,zc,-yc),(l,h,w))
    
def getresource(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),'resources',name)

def main(args=None):
    parser = argparse.ArgumentParser(description='Visualize loadbuilding solutions')
    parser.add_argument('--instance',     '-I',  metavar='INPUT_FILE',    required=True,                           help='The instance file')
    parser.add_argument('--instancetype', '-IT', metavar='INSTANCE_TYPE', choices=['json', 'xml', 'yaml'],         help='The type of the instance file, choose one of: json, xml, yaml')
    parser.add_argument('--solution',     '-S',  metavar='SOLUTION_FILE', required=True,                           help='The solution file')
    parser.add_argument('--solutiontype', '-ST', metavar='SOLUTION_TYPE', choices=['json', 'xml', 'yaml'],         help='The type of the solution file, choose one of: json, xml, yaml')
    parser.add_argument('--color',        '-C',  metavar='COLOR',         choices=['file', 'correct', 'distinct'], help='The coloring option, choose one of: file, correct, distinct')
    parser.add_argument('--opacity',      '-O',  metavar='OPACITY',       required=False,                          help='The default opacity')
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
    if args.color is None:
        args.color = 'file'
    if args.opacity is None:
        args.opacity = 0.5

    converter = LoadbuildSolution.LoadbuildSolution(args.instance,args.instancetype,args.solution,args.solutiontype, "SolutionViewer", "-")
    
    def button(label="",bgimage=""):
        if bgimage != "":
            bgimage = "background-image: url(" + bgimage + ");"
        return "<span style='background-color: black; " + bgimage + " background-repeat: no-repeat; background-position: center; border-radius: 5px; color: white; font-weight: bold; height: 20px; min-width: 30px; margin: 5px; padding: 5px 10px 5px;'>" + label + "</span>"

    import colorsys
    def getColor(n, total):
        RGB = colorsys.hsv_to_rgb(n/total, 0.9, 0.9)
        return vpython.vec(*RGB)

    def render(obj, loadingspace, n):
            L,W,H = loadingspace.boundingBox
            scene = vpython.canvas()
            scene.title = ("<h1>" + obj.TypeString().capitalize() + " with id " + str(obj.id) + "</h1>" if n == 0 else "") + "<h2>Loadingspace with id " + str(loadingspace.id) + "</h2>"
            scene.background = vpython.color.white
            scene.center  = vpython.vec(L/2,H/2,-W/2)
            scene.forward = vpython.vec(0.0, 0.0, -1.0)
            scene.append_to_caption(
"<table style='border-collapse: collapse;'><tr><th>Control</th><th>Function</th></tr>" +\
"<tr style='border-bottom: 1px solid black;'><td style='text-align: center;'><div style='margin-top: 15px; margin-bottom: 15px;'>" + r_drag + "</div><div style='margin-top: 15px; margin-bottom: 15px;'>" + ctrl   + "+" + l_drag + "</div></td><td style='text-align: center;'>Rotate</td></tr>" +\
"<tr style='border-bottom: 1px solid black;'><td style='text-align: center;'><div style='margin-top: 15px; margin-bottom: 15px;'>" + m_drag + "</div><div style='margin-top: 15px; margin-bottom: 15px;'>" + alt    + "+" + l_drag + "</div><div style='margin-top: 15px; margin-bottom: 15px;'>" + option + "+" + l_drag + "</div><div style='margin-top: 15px; margin-bottom: 15px;'>" + b_drag + "</div></td><td style='text-align: center;'>Zoom</td></tr>" +\
"<tr style='border-bottom: 1px solid black;'><td style='text-align: center;'><div style='margin-top: 15px; margin-bottom: 15px;'>" + shift  + "+" + l_drag + "</div></td><td style='text-align: center;'>Pan</td></tr></table>")

            for i,placement in enumerate(loadingspace.placements):
                if args.color == 'file':
                    if placement.color is not None:
                        if len(placement.color) != 7 and len(placement.color) != 9 or\
                           placement.color[0] != "#" or\
                           any(map((lambda c: c.upper() not in ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]),placement.color[1:])):
                            raise Exception("Incorrectly formatted color attribute for placement with id " + str(placement.id))
                        c = vpython.vec(int(placement.color[1:3],16)/255, int(placement.color[3:5],16)/255, int(placement.color[5:7],16)/255)
                        o = args.opacity
                        if len(placement.color) == 9:
                            o = int(placement.color[7:],16)/255
                    else:
                        c = vpython.vec(0.9,0.9,0.9)
                        o = args.opacity
                elif args.color == 'correct':
                    if placement.correct:
                        c = vpython.vec(0, 1, 0)
                        o = args.opacity
                    else:
                        c = vpython.vec(1, 0, 0)
                        o = 1
                else:
                    c = getColor(i, len(loadingspace.placements))
                    o = 1
                x1 = placement.position
                x2 = [x + l for x,l in zip(x1, placement.boundingBox)]
                b = placement_to_box((x1,x2))
                vpython.box(pos=vpython.vec(*b[0]), size=vpython.vec(*b[1]), color=c, opacity=o)
            
#            from ortec.scientific.benchmarks.loadbuilding.common.constraints import ReadableItemLabelConstraint.ReadableItemLabelConstraint as ReadableItemLabelConstraint
#            for dummy in ReadableItemLabelConstraint.GetDummies(loadingspace):
#                x1 = dummy.position
#                x2 = [x + l for x,l in zip(x1, dummy.boundingBox)]
#                b = placement_to_box((x1,x2))
#                box(pos=vec(*b[0]), size=vec(*b[1]), color=vec(1,0,0), opacity=0.1)
                
            beam = 0.002*max(L,W,H)
            vpython.box(pos=vpython.vec(L/2,-beam/2,-W/2), size=vpython.vec(L,beam,W), color=vpython.vec(0.8,0.8,0.8))
            vpython.box(pos=vpython.vec(  - beam/2, H/2,             beam/2), size=vpython.vec(beam,H+2*beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(  - beam/2, H/2,        -W - beam/2), size=vpython.vec(beam,H+2*beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L + beam/2, H/2,             beam/2), size=vpython.vec(beam,H+2*beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L + beam/2, H/2,        -W - beam/2), size=vpython.vec(beam,H+2*beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L/2,        H + beam/2, -W - beam/2), size=vpython.vec(L,beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L/2,        H + beam/2,      beam/2), size=vpython.vec(L,beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L/2,          - beam/2, -W - beam/2), size=vpython.vec(L,beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L/2,          - beam/2,      beam/2), size=vpython.vec(L,beam,beam), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L + beam/2, H + beam/2, -W/2),        size=vpython.vec(beam,beam,W), color=vpython.color.black)
            vpython.box(pos=vpython.vec(  - beam/2, H + beam/2, -W/2),        size=vpython.vec(beam,beam,W), color=vpython.color.black)
            vpython.box(pos=vpython.vec(L + beam/2,   - beam/2, -W/2),        size=vpython.vec(beam,beam,W), color=vpython.color.black)
            vpython.box(pos=vpython.vec(  - beam/2,   - beam/2, -W/2),        size=vpython.vec(beam,beam,W), color=vpython.color.black)
            
            M = min(L,W,H)
            vpython.arrow(pos=vpython.vec(0, 0, 0), axis=vpython.vec(+M/4,+0,+0), color=vpython.color.red)
            vpython.arrow(pos=vpython.vec(0, 0, 0), axis=vpython.vec(+0,+M/4,+0), color=vpython.color.blue)
            vpython.arrow(pos=vpython.vec(0, 0, 0), axis=vpython.vec(+0,+0,-M/4), color=vpython.color.green)
            vpython.box(pos=vpython.vec(0, 0, 0), size=vpython.vec(M/20,M/20,M/20), color=vpython.color.black)

    shift  = button("&#x21E7; Shift")
    ctrl   = button("Ctrl")
    alt    = button("Alt")
    option = button("&#x2325; Option")
    if LooseVersion(vpython.__version__) > LooseVersion("7.4.4"):
        l_drag = button(bgimage=getresource("left.png"))
        r_drag = button(bgimage=getresource("right.png"))
        b_drag = button(bgimage=getresource("both.png"))
        m_drag = button(bgimage=getresource("middle.png"))
    else:
        l_drag = button("left mouse button")
        r_drag = button("right mouse button")
        b_drag = button("left+right mouse button")
        m_drag = button("middle mouse button")
    for container in converter.lbSolution.containers:
        for n,loadingspace in enumerate(container.loadingspaces):
            render(container, loadingspace, n)
    for pallet in converter.lbSolution.pallets:
        render(pallet, pallet.loadingspace, 0)
    for box in converter.lbSolution.boxes:
        render(box, box.loadingspace, 0)
                            
    while True:
        vpython.rate(1)

if __name__=="__main__":
    exit("Don't run this file")