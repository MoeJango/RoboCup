import numpy as np

def zerosCovered(costArr, coveredArr):
    for i in range(11):
        for j in range(11):
            if costArr[i][j] == 0 and not coveredArr[i][j] == 1:
                return [i, j]
    return -1


def coverings(costArr, coveredArr, starredZeros, primedZeros):
    isCovered = zerosCovered(costArr, coveredArr)
    while not isCovered == -1:
        primedZeros[isCovered[0]][isCovered[1]] = 1
        if np.any(starredZeros[isCovered[0], :]):
            for k in range(11):
                if starredZeros[isCovered[0]][k] == 1:
                    for c in range(11):
                        if not np.all(coveredArr[c, :] == 1):
                            coveredArr[c][k] = 0
                    coveredArr[isCovered[0], :] = 1
                    break
        else:
            path = np.zeros((11, 11))
            currRow = isCovered[0]
            currCol = isCovered[1]
            path[currRow][currCol] = 1
            
            while True:
                if not np.any(starredZeros[:, currCol]):
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
            primedZeros.fill(0)
            coveredArr.fill(0)
            for i in range(11):
                for j in range(11):
                    if starredZeros[i][j] == 1:
                        coveredArr[:, j] = 1
        isCovered = zerosCovered(costArr, coveredArr)

    
    starred = 0
    for i in range(11):
        for j in range(11):
            if starredZeros[i][j] == 1:
                starred += 1
    
    return starred


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

    for i in range(11):
            for j in range(11):
                if starredZeros[i][j] == 1:
                    coveredArr[:, j] = 1 

    starred = coverings(costArr, coveredArr, starredZeros, primedZeros)
    
    while starred < 11:
        minVal = np.min(costArr[np.where(coveredArr == 0)])
    
        for i in range(11):
            if not np.all(coveredArr[i, :] == 1):
                costArr[i, :] -= minVal
            if np.all(coveredArr[:, i] == 1):
                costArr[:, i] += minVal
        starred = coverings(costArr, coveredArr, starredZeros, primedZeros)
        

    point_preferences = {}

    for i in range(11):
        for j in range(11):
            if starredZeros[i][j] == 1:
                point_preferences[i+1] = formation_positions[j]

    return point_preferences


def pass_reciever_selector(player_unum, teammate_positions, final_target):
    
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#

    # Example
    pass_reciever_unum = player_unum + 1 

    if pass_reciever_unum != 12:
        target = teammate_positions[pass_reciever_unum-1] #This is 0 indexed so we actually need to minus 1 
    else:
        target = final_target 
    
    return target


