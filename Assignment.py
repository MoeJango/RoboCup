import numpy as np

def zerosCovered(costArr, coveredArr, starredZeros):
    for i in range(11):
            for j in range(11):
                if starredZeros[i][j] == 1:
                    coveredArr[:, j] = 1

    for i in range(11):
        for j in range(11):
            if costArr[i][j] == 0 and not coveredArr[i][j] == 1:
                return False
    return True


def coverings(costArr, coveredArr, starredZeros, primedZeros):
    while not zerosCovered(costArr, coveredArr, starredZeros):
        for i in range(11):
            elseHit = False
            for j in range(11):
                if costArr[i][j] == 0 and not coveredArr[i][j] == 1:
                    primedZeros[i][j] = 1
                    if np.any(starredZeros[i, :]):
                        for k in range(11):
                            if starredZeros[i][k] == 1:
                                coveredArr[:, k] = 0
                                coveredArr[i, :] = 1
                                break
                    else:
                        elseHit = True
                        path = np.zeros((11, 11))
                        path[i][j] = 1
                        currRow = i
                        currCol = j
        
                        while True:
                            if not np.any(starredZeros[currRow, :]):
                                break
                            for k in range(11):
                                if starredZeros[k][currCol] == 1:
                                    path[k][currCol] = 1
                                    currRow = k
                                    break
                            for k in range(11):
                                if primedZeros[currRow][k] == 1:
                                    path[currRow][k] = 1
                                    currCol = k
                                    break
                        for i in range(11):
                            for j in range(11):
                                if path[i][j] == 1 and starredZeros[i][j] == 1:
                                    starredZeros[i][j] = 0
                                if path[i][j] == 1 and primedZeros[i][j] == 1:
                                    starredZeros[i][j] = 1
                        primedZeros = np.zeros((11, 11))
                        coveredArr = np.zeros((11, 11))
                        break
            if elseHit:
                break
    
    lines = 0
    for i in range(11):
        if np.all(coveredArr[i, :] == 1):
            lines += 1
    for j in range(11):
        if np.all(coveredArr[:, j] == 1):
            lines += 1
    return lines


def role_assignment(teammate_positions, formation_positions): 

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#

    costArr = np.zeros((11, 11))
    starredZeros = np.zeros((11, 11))
    primedZeros = np.zeros((11, 11))
    coveredArr = np.zeros((11, 11))

    for i in range(len(teammate_positions)):
        for j in range(len(formation_positions)):
            costArr[i][j] = np.linalg.norm(teammate_positions[i] - formation_positions[j])

    for i in range(11):
        costArr[i, :] -= np.min(costArr[i, :])
    for j in range(11):
        costArr[:, j] -= np.min(costArr[:, j])

    for i in range(11):
        for j in range(11):
            if costArr[i][j] == 0 and not np.any(starredZeros[i, :]) and not np.any(starredZeros[:, j]):
                starredZeros[i][j] = 1
                break

    lines = coverings(costArr, coveredArr, starredZeros, primedZeros)
    while lines < 11:
        minVal = np.min(costArr[np.where(coveredArr == 0)])
        for i in range(11):
            if np.all(coveredArr[i, :] == 0):
                costArr[i, :] -= minVal
            if np.all(coveredArr[:, i] == 1):
                costArr[:, i] += minVal
        lines = coverings(costArr, coveredArr, starredZeros, primedZeros)
        

    point_preferences = {}

    rowMask = np.zeros(11)
    colMask = np.zeros(11)
    minRow = -1
    minRowCount = 100

    for i in range(11):
        if rowMask[i] == 1:
            continue
        thisRowCount = 0
        for j in range(11):
            if colMask[j] == 1:
                continue
            if costArr[i][j] == 0:
                thisRowCount += 1
        if thisRowCount < minRowCount:
            minRowCount = thisRowCount
            minRow = i
    
    rowMask[minRow] = 1
    for j in range(11):
        if costArr[minRow][j] == 0:
            colMask[j] = 1
            point_preferences[minRow + 1] = formation_positions[j]


    return point_preferences


def pass_reciever_selector(player_unum, teammate_positions, final_target):
    
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#

    # Example
    pass_reciever_unum = player_unum + 1                  #This starts indexing at 1, therefore player 1 wants to pass to player 2
    
    if pass_reciever_unum != 12:
        target = teammate_positions[pass_reciever_unum-1] #This is 0 indexed so we actually need to minus 1 
    else:
        target = final_target 
    
    return target

