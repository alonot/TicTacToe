
import copy


def printBoard(board:list):

    print()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                print('X',end='|')
            elif board[i][j] == 2:
                print('O',end='|')
            else:
                print(' ',end='|')
        print()
        print('__'*len(board[0]))

    print()


def CheckScore(curPossibilites,newPos) -> int:
    
    wasTwo = False
    toAdd = []
    for lines in curPossibilites:
        if len(lines) == 1:
            slope = (abs(lines[0][0] - newPos[0]),abs(lines[0][1] - newPos[1]))

            if slope[0] == 0 or slope[1] == 0 or slope[1]//slope[0] == 1:
                 toAdd.append(lines + [newPos])
                 wasTwo = True # we cannot return here , there main be many twos

        elif len(lines) == 2:
            slopeWithPos = ((lines[0][0] - newPos[0]),(lines[0][1] - newPos[1]))
            slope = ((lines[0][0] - lines[1][0]),(lines[0][1] - lines[1][1]))

            if slope[0] == 0 or slopeWithPos[0] ==0:
                if slope[0] == 0 and slopeWithPos[0] ==0:
                    curPossibilites.append(lines + [newPos])
                    # print("Is",lines+[newPos])
                    return 3
            elif  (slope[1] / slope[0]) == (slopeWithPos[1] / slopeWithPos[0]):
                curPossibilites.append(lines + [newPos])
                # print("Is1",lines+[newPos],slope,slopeWithPos)
                return 3
            
    curPossibilites.append([(newPos)])
    curPossibilites+=toAdd
    if wasTwo:
        return 2
    return 1

def getEmptyLoc(board):
    emptyLoc = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                emptyLoc.append((i,j))

    return emptyLoc        



def removePos (curPossi, pos):
    newLst = []
    for index in range(len(curPossi)):
        # print(curPossi[index],pos not in curPossi[index])
        if pos not in curPossi[index]:
            newLst.append(curPossi[index])
    # print(pos,newLst)
    return copy.deepcopy(newLst)


def NextMove1(board,curPossibilitiesX,curPossibilitiesO):
    copyO =copy.deepcopy(curPossibilitiesO)
    copyX= copy.deepcopy(curPossibilitiesX)
    frontierList = []
    parentDict = {}
    score = {}
    emptyLocs = getEmptyLoc(board)
    for locs in emptyLocs:
        frontierList.append((locs,None))
    # print(emptyLocs)

    final = []
    depth = 0

    while len(frontierList) != 0:
        nextElement = frontierList[0]
        frontierList = frontierList[1:]

        newPos = nextElement[0]
        parent = nextElement[1]

        if newPos in emptyLocs:
            emptyLocs.remove(newPos)
        hasWon = False
        parentDict[newPos] = parent

        if depth % 2 == 0 :
            if (CheckScore(curPossibilites=curPossibilitiesO, newPos=newPos) == 3):
                if parent == None:
                    parent = newPos
                tempFL = []
                for node in frontierList:
                    if node[1] != parent:
                        tempFL.append(node)

                frontierList = tempFL
                
                if parent in score.keys():
                    score[parent].append(depth+1)
                else:
                    score[parent] = [depth + 1]

                # print("O",curPossibilitiesO,file= file)
                curPossibilitiesO = removePos(curPossibilitiesO, newPos)
                emptyLocs.append(newPos)

                hasWon = True
        else:
            if (CheckScore(curPossibilites=curPossibilitiesX, newPos=newPos) == 3):
                if parent == None:
                    parent = newPos

                tempFL = []
                for node in frontierList:
                    if node[1] != parent:
                        tempFL.append(node)

                frontierList = tempFL
                
                if parent in score.keys():
                    score[parent].append(20+depth+1)
                else:
                    score[parent] = [20 + depth + 1]
                # print("X",curPossibilitiesX,file= file)
                curPossibilitiesX = removePos(curPossibilitiesX, newPos)
                
                emptyLocs.append(newPos)

                hasWon = True
            
        
        isParentPresent = False
        # print(parentDict)
        if parent != None:
            while parentDict.get(parent) != None:
                # print(parent,newPos)
                # This algorithm take loss as loss it does not discriminate that is in which strategy we are losing first.
                

                for node in frontierList:
                    if node[1] == parent:
                        isParentPresent = True
                        break

                if isParentPresent or (len(emptyLocs) != 0 and not hasWon):
                    break

                

                if parent not in score.keys():
                    # print("Y",depth ,file= file)
                    emptyLocs.append(newPos)
                    hasWon = True
                    if(depth % 2 == 0):
                        curPossibilitiesO = removePos(curPossibilitiesO,newPos)
                    else:
                        curPossibilitiesX = removePos(curPossibilitiesX,newPos)
                    score[parent] = [11]

                if depth % 2 == 0:
                    # This parent is min
                    score[parent] = [min(score[parent])]
                    curPossibilitiesX = removePos(curPossibilitiesX,parent)
                    emptyLocs.append(parent)
                else:

                    score[parent] = [max(score[parent])]
                    curPossibilitiesO = removePos(curPossibilitiesO, parent)
                    emptyLocs.append(parent)
                
                # print(parent,parentDict[parent])
                if parentDict[parent] in score.keys():
                    score[parentDict[parent]].append(score[parent][0]) 
                else:
                    score[parentDict[parent]] = [score[parent][0]]

                del score[parent]

                depth -=1
                prevParent = parent
                parent = parentDict[parent]
                
                del parentDict[prevParent]

        

        if not hasWon:
            depth +=1
            for loc in emptyLocs:
                frontierList = [(loc,newPos)] + frontierList
                parentDict[loc] = newPos
            # print(frontierList)
                

        if parentDict.get(parent) == None:
            onlyNone = True
            for node in frontierList:
                if node[1] != None:
                    # print("tr",node)    
                    onlyNone = False
                    break
            
            if onlyNone:
                if parent not in score.keys():
                    final.append((11,parent))
                else:
                    final.append((max(score[parent]),parent))
                    del score[parent]
                emptyLocs.append(parent)
                depth = 0

                if depth % 2 == 0:
                    # This parent is min
                    curPossibilitiesO = removePos(curPossibilitiesO, parent)
                else:
                    curPossibilitiesX = removePos(curPossibilitiesX, parent)

                parent = {}


    print(final)
    print(curPossibilitiesO)
    print(curPossibilitiesX)
    # file.close()

    pos = ((0,0))
    final.sort()
    if final[0][0] >= 20:
        pos = final.pop()[1]
    else:
        pos = final[0][1]
        
    return [pos,copyO,copyX]




Board = [[0,0,0] for i in range(3)]
emptyPlaces = [(i,j) for j in range(len(Board[1])) for i in range(len(Board))]
currentChance = 'X'
possibX=[]
possibY=[]
cur = 2

# f = open ('out.txt','w')
# print("",file=f)
# f.close()

print('Enter the pos as `i j` ')
while len(emptyPlaces) > 0:

    try:
        inp = input(f'${currentChance} : ')
        response  = [(int)(i) for i in inp.split()]
        if len(response) != 2:
            raise SyntaxError("2 elements please")
    except Exception as e:
        print("Something went wrong.(probably your syntax) =>",e)
        printBoard(Board)
        continue
    if  response[0] >= len(Board) or response[0] < 0 or response[1] < 0 or response[1] >= len(Board[0]):
        print("Out of Bounds\nTry again")
        printBoard(Board)
        continue

    if Board[response[0]][response[1]] != 0:
        print("Already Occupied")
        printBoard(Board)
        continue
    # if currentChance == 'X':
        # currentChance = 'O'
    Board[response[0]][response[1]] = 1
    if CheckScore(possibX,response) == 3:
        print("X won")
        printBoard(Board)
        print("X",possibX)
        print("O",possibY)
        exit(0)
    emptyPlaces.remove(tuple(response))

    if len(emptyPlaces) == 0:
        printBoard(Board)
        print("Match drawn")
        exit(0) 

    # else:
    nextPos,possibY,possibX = NextMove1(Board,possibX,possibY)
    Board[nextPos[0]][nextPos[1]] = cur
    if (CheckScore(possibY,nextPos)) == 3:
        print('O won')
        printBoard(Board)
        print("X",possibX)
        print("O",possibY)
        exit(0)
    


    printBoard(Board)
    print("="*100)
    print("X",possibX)
    print("O",possibY)
    emptyPlaces.remove(tuple(nextPos))



    


