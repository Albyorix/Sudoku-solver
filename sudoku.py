from copy import deepcopy
import time
import cProfile
import pp

def get_positionXY(Z):
    """
    Returns X and Y list values
    for the corresponding Z case.
    """
    if Z == 0:
        return [0,1,2], [0,1,2]
    if Z == 1:
        return [0,1,2], [3,4,5]
    if Z == 2:
        return [0,1,2], [6,7,8]
    if Z == 3:
        return [3,4,5], [0,1,2]
    if Z == 4:
        return [3,4,5], [3,4,5]
    if Z == 5:
        return [3,4,5], [6,7,8]
    if Z == 6:
        return [6,7,8], [0,1,2]
    if Z == 7:
        return [6,7,8], [3,4,5]
    if Z == 8:
        return [6,7,8], [6,7,8]

def transform_lineToMatrix(sudokuLine):
    sudokuList = list(sudokuLine)
    return sudokuList

class Case:

    def __init__(self, positionX, positionY, value='.'):
        self.positionX = positionX
        self.positionY = positionY
        self.positionZ = 0
        if self.positionX < 3:
            if self.positionY < 3:
                self.positionZ = 0
            if 3 <= self.positionY < 6:
                self.positionZ = 1
            if self.positionY > 5:
                self.positionZ = 2
        if 3 <= self.positionX < 6:
            if self.positionY < 3:
                self.positionZ = 3
            if 3 <= self.positionY < 6:
                self.positionZ = 4
            if self.positionY > 5:
                self.positionZ = 5
        if self.positionX > 5:
            if self.positionY < 3:
                self.positionZ = 6
            if 3 <= self.positionY < 6:
                self.positionZ = 7
            if self.positionY > 5:
                self.positionZ = 8
        self.value = value
        if value == '.':
            self.possibleValues = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
            self.possibleValues = []
        self.valuesLeft = 9

    def __repr__(self):
        rep = str(self.value) + str(self.possibleValues) + "\n"
        return rep

    def add_value(self, value):
        self.value = value
        self.possibleValues = []


class Sudoku:

    def __init__(self, matrix):
        self.matrix = matrix
        for i in xrange(9):
            for j in xrange(9):
                self.matrix[i*9+j] = Case(i, j, matrix[i*9+j])
        self.caseSolved = self.get_numberOfCasesSolved()

    def __repr__(self):
        rep = 'Current SUDOKU\n'
        rep += str(self.caseSolved) + ' case solved\n'
        for i in xrange(9):
            if i in [3,6]:
                rep += "\n"
            for j in xrange(9):
                if j in [3,6]:
                    rep += "|  "
                rep += "|" + self.matrix[i*9+j].value
            rep += "|\n"
        #for i in xrange(9):
        #    for j in xrange(9):
        #        rep += self.matrix[i*9+j].__repr__()
        return rep

    def deepcopy(self):
        sudokuLine = ''
        for i in xrange(9):
            for j in xrange(9):
                sudokuLine += self.matrix[i*9+j].value
        #print sudokuLine
        return Sudoku(transform_lineToMatrix(sudokuLine))

    def add_value(self, currentCase, value):
        self.caseSolved += 1
        currentCase.add_value(value)

    def get_numberOfCasesSolved(self):
        count = 0
        for i in xrange(9):
            for j in xrange(9):
                if self.matrix[i*9+j].value != '.':
                    count += 1
        return count

    def check_if_finished(self):
        for i in xrange(9):
            for j in xrange(9):
                if self.matrix[i*9+j].value == '.':
                    return False
        return True

    def check_if_grid_possible(self):
        for i in xrange(9):
            for j in xrange(9):
                if self.matrix[i*9+j].valuesLeft == 0:
                    return False
        for j in xrange(9):
            seenX, seenY, seenZ = [], [], []
            for i in xrange(9):
                if self.matrix[i*9+j].value in seenX:
                    return False
                elif self.matrix[i*9+j].value != ".":
                    seenX.append(self.matrix[i*9+j].value)
                if self.matrix[j*9+i].value in seenY:
                    return False
                elif self.matrix[j*9+i].value != ".":
                    seenY.append(self.matrix[j*9+i].value)
            X, Y = get_positionXY(j)
            for i in X:
                for k in Y:
                    if self.matrix[i*9+k].value in seenZ:
                        return False
                    elif self.matrix[i*9+k].value != ".":
                        seenZ.append(self.matrix[i*9+k].value)
        return True

    def check_rule1(self, positionX, positionY):
        currentCase = self.matrix[positionX*9+positionY]
        if currentCase.value != '.':
            return
        possibleValues = currentCase.possibleValues
        for i in xrange(9):
            value = self.matrix[i*9+positionY].value
            if value != '.' and value in possibleValues:
                possibleValues.remove(value)
            value = self.matrix[positionX*9+i].value
            if value != '.' and value in possibleValues:
                possibleValues.remove(value)
        X, Y = get_positionXY(currentCase.positionZ)
        for i in X:
            for j in Y:
                value = self.matrix[i*9+j].value
                if value != '.' and value in possibleValues:
                    possibleValues.remove(value)
        self.check_valuesLeft(positionX, positionY)

    def check_valuesLeft(self, positionX, positionY):
        currentCase = self.matrix[positionX*9+positionY]
        count = len(currentCase.possibleValues)
        if count == 1:
            self.add_value(currentCase, currentCase.possibleValues[0])
        else:
            currentCase.valuesLeft = count

    def check_rule2(self, positionX, positionY):
        currentCase = self.matrix[positionX*9+positionY]
        otherCasesPossibilitiesX = []
        for i in xrange(9):
            if i != positionX:
                otherCasesPossibilitiesX += self.matrix[i*9+positionY].possibleValues
        otherCasesPossibilitiesY = []
        for j in xrange(9):
            if j != positionY:
                otherCasesPossibilitiesY += self.matrix[positionX*9+j].possibleValues
        otherCasesPossibilitiesZ = []
        X, Y = get_positionXY(currentCase.positionZ)
        for i in X:
            for j in Y:
                if i != positionX and j != positionY:
                    otherCasesPossibilitiesZ += self.matrix[i*9+j].possibleValues
        for value in currentCase.possibleValues:
            if not value in otherCasesPossibilitiesX \
                    and not value in otherCasesPossibilitiesY \
                    and not value in otherCasesPossibilitiesZ:
                self.add_value(currentCase, value)
                self.update_dicosWithNewValue(positionX, positionY, value)

    def update_dicosWithNewValue(self, positionX, positionY, value):
        for i in xrange(9):
            if i != positionX and value in self.matrix[i*9+positionY].possibleValues:
                self.matrix[i*9+positionY].possibleValues.remove(value)
        for j in xrange(9):
            if j != positionY and value in self.matrix[positionX*9+j].possibleValues:
                self.matrix[positionX*9+j].possibleValues.remove(value)
        X, Y = get_positionXY(self.matrix[positionX*9+positionY].positionZ)
        for i in X:
            for j in Y:
                if i != positionX and j != positionY and value in self.matrix[i*9+j].possibleValues:
                    self.matrix[i*9+j].possibleValues.remove(value)

    def test_grid_rule1(self):
        for i in xrange(9):
            for j in xrange(9):
                self.check_rule1(i, j)

    def test_grid_rule2(self):
        for i in xrange(9):
            for j in xrange(9):
                self.check_rule2(i, j)

    def test_grid_deterministic(self):
        oldCaseSolved = 0
        newCaseSolved = self.caseSolved
        while newCaseSolved - oldCaseSolved > 0:
            oldCaseSolved = newCaseSolved
            self.test_grid_rule1()
            newCaseSolved = self.caseSolved
        #self.test_grid_rule2() # It less efficient in time with this rule
        newCaseSolved = self.caseSolved
        if newCaseSolved - oldCaseSolved > 0:
            self.test_grid_deterministic()

    def get_best_case_for_guess(self):
        smallestLenth = 10
        positionX, positionY, bestPossibilities = 0, 0, None
        for i in xrange(9):
            for j in xrange(9):
                if not self.matrix[i*9+j].possibleValues == []:
                    possibilities =  self.matrix[i*9+j].possibleValues
                    if len(possibilities) < smallestLenth:
                        smallestLenth = len(possibilities)
                        positionX, positionY, bestPossibilities = i, j,possibilities
                        if smallestLenth == 2:
                            return positionX, positionY, bestPossibilities
        return positionX, positionY, bestPossibilities

    def test_grid_withGuess(self):
        self.test_grid_deterministic()
        goodCases = self.get_good_guess()
        if goodCases == []:
            print "There is an error in the grid"
        else:
            for case in goodCases:
                positionX, positionY, guess = case
                self.add_value(self.matrix[positionX*9+positionY], guess)
            self.test_grid_deterministic()
            if not self.check_if_finished():
                print "There was an error with gooCases"
            else:
                pass # print "YOU WIN"

    def get_good_guess(self):
        positionX, positionY, possibilities = self.get_best_case_for_guess()
        for guess in possibilities:
            newsudoku = self.deepcopy()
            newsudoku.add_value(newsudoku.matrix[positionX*9+positionY], guess)
            newsudoku.test_grid_deterministic()
            if newsudoku.check_if_grid_possible():
                if newsudoku.check_if_finished():
                    goodCases = [ (positionX, positionY, guess)]
                    return goodCases
                else:
                    goodCases = newsudoku.get_good_guess()
                    if len(goodCases) > 0:
                        goodCases.append( (positionX, positionY, guess))
                        return goodCases
        return []


if __name__ == '__main__':

    totalEntry = time.clock()
    sudokuFile = open('top870.txt')
    def solve_sudoku(line):
        mySudoku = transform_lineToMatrix(line)
        sudoku = Sudoku(mySudoku)
        sudoku.test_grid_withGuess()
        return sudoku


    totalEntry = time.clock()
    SaveList = []
    job_server = pp.Server(ppservers=("*",))
    line = '.'
    while line != '':
        line = sudokuFile.readline()
        job = job_server.submit(solve_sudoku, (line,), (transform_lineToMatrix, Sudoku, Case, get_positionXY), ('time',))
        SaveList.append( job) # DO NOT USE THE PARENTHESIS HERE
    for job in SaveList:
        print job() # USE PARENTHESIS HERE
    print "Parallel Python ", time.clock() - totalEntry
