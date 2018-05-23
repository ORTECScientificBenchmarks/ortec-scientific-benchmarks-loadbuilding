class NgoiMatrix(object):
    def __init__(self, L, W, H):
        self.length = L
        self.width  = W
        self.height = H
        self.xs = [0, L]
        self.ys = [0, W]
        self.ngoi = [[[0, []]]]
        self.outside_report = list()
        self.overlap_report = list()
        self.support_report = list()
        self.overlaps = set()
        self.outside_valid = True
        self.overlap_valid = True
        self.support_valid = True
    
    def SplitHorizontally(self, x):
        previous_x = 0
        for i,current_x in enumerate(self.xs):
            if x == current_x:
                break
            if x > previous_x and x < current_x:
                self.xs.insert(i,x)
                for row in self.ngoi:
                    row.insert(i-1, row[i-1])
                break
            previous_x = current_x
    
    def SplitVertically(self, y):
        previous_y = 0
        for i,current_y in enumerate(self.ys):
            if y == current_y:
                break
            if y > previous_y and y < current_y:
                self.ys.insert(i,y)
                self.ngoi.insert(i-1, list(self.ngoi[i-1]))
                break
            previous_y = current_y
            
    def GetIndices(self, X1, X2):
        x1, y1 = X1
        x2, y2 = X2
        x_indices = []
        for i,x in list(enumerate(self.xs))[:-1]:
            if x >= x2:
                break
            if x >= x1:
                x_indices.append(i)
        y_indices = []
        for j,y in list(enumerate(self.ys))[:-1]:
            if y >= y2:
                break
            if y >= y1:
                y_indices.append(j)
        return x_indices, y_indices
    
    # Cuboids are defined by two corner points, and they should be added in increasing z-order
    def addCuboid(self, placement):
        x1,y1,z1 = placement.position
        x2,y2,z2 = [coord+length for coord,length in zip(placement.position, placement.boundingBox)]
        name = placement.TypeString().capitalize() + " with id " + str(placement.id)
        if x1 < 0 or y1 < 0 or z1 < 0 or x1 > self.length or y1 > self.width or z1 > self.height or\
           x2 < 0 or y2 < 0 or z2 < 0 or x2 > self.length or y2 > self.width or z2 > self.height:
            self.outside_valid = False
            self.outside_report.append(name + " lies outside its loadingspace <- VIOLATION")
            placement.correct = False
        else:
            self.outside_report.append(name + " lies inside its loadingspace")
        self.SplitHorizontally(x1)
        self.SplitHorizontally(x2)
        self.SplitVertically(y1)
        self.SplitVertically(y2)
        x_ind, y_ind = self.GetIndices((x1,y1), (x2,y2))
        supported_area = 0
        for i in x_ind:
            for j in y_ind:
                if self.ngoi[j][i][0] > z1:
                    self.overlap_valid = False
                    placement.correct = False
                    for z,old_placement in self.ngoi[j][i][1]:
                        if z+old_placement.boundingBox[2] > z1:
                            old_placement.correct = False
                            old_name = old_placement.TypeString() + " with id " + str(old_placement.id)
                            names = tuple(sorted([old_name, name.lower()]))
                            if names not in self.overlaps:
                                self.overlaps.add(names)
                                self.overlap_report.append(names[0].capitalize() + " overlaps with " + names[1] + " <- VIOLATION")
                else:
                    if self.ngoi[j][i][0] == z1:
                        supported_area += (self.xs[i+1] - self.xs[i])*(self.ys[j+1] - self.ys[j])
                self.ngoi[j][i] = [z2, self.ngoi[j][i][1] + [[z1, placement]]]
        total_area = (x2 - x1)*(y2 - y1)
        if total_area != 0:
            if supported_area < placement.support*total_area:
                self.support_valid = False
                self.support_report.append(name + " is supported by " + str(supported_area/total_area) + " of required " + str(placement.support) + " <- VIOLATION")
                placement.correct = False
            else:
                self.support_report.append(name + " is supported by " + str(supported_area/total_area) + " of required " + str(placement.support))
    
if __name__=="__main__":
    exit("Don't run this file")
