import numpy as np

def zerosCovered(costArr, coveredArr, starredZeros):
    for i in range(11):
            for j in range(11):
                if starredZeros[i][j] == 1:
                    coveredArr[:, j] = 1

    for i in range(11):
        for j in range(11):
            if costArr[i][j] == 0 and not coveredArr[i][j] == 1:
                return [i, j]
    return -1


def coverings(costArr, coveredArr, starredZeros, primedZeros):
    isCovered = zerosCovered(costArr, coveredArr, starredZeros)
    while not isCovered == -1:
        primedZeros[isCovered[0]][isCovered[1]] = 1
        if np.any(starredZeros[isCovered[0], :]):
            for k in range(11):
                if starredZeros[isCovered[0]][k] == 1:
                    coveredArr[:, k] = 0
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
            primedZeros = np.zeros((11, 11))
            coveredArr = np.zeros((11, 11))
            isCovered = zerosCovered(costArr, coveredArr, starredZeros)
            break
        isCovered = zerosCovered(costArr, coveredArr, starredZeros)
    
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
    

    while len(point_preferences) < 11:
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
            if colMask[j] == 1:
                continue
            if costArr[minRow][j] == 0:
                colMask[j] = 1
                point_preferences[minRow + 1] = formation_positions[j]
                break

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


teammate_positions = np.array([ np.array([3.74540119, 9.50714306]),
  np.array([7.31993942, 5.98658484]),
  np.array([1.5601864, 1.5599452]),
  np.array([0.58083612, 8.66176146]),
  np.array([6.01115012, 7.08072578]),
  np.array([0.20584494, 9.69909852]),
  np.array([8.32442641, 2.12339111]),
  np.array([1.81824967, 1.8340451 ]),
  np.array([3.04242243, 5.24756432]),
  np.array([4.31945019, 2.9122914 ]),
  np.array([6.11852895, 1.39493861]) ])

# Formation positions as 11 2-element numpy arrays
formation_positions = np.array([ np.array([2.92144649, 3.66361843]),
  np.array([4.56069984, 7.85175961]),
  np.array([1.99673782, 5.14234438]),
  np.array([5.92414569, 0.46450413]),
  np.array([6.07544852, 1.70524124]),
  np.array([0.65051593, 9.48885537]),
  np.array([9.65632033, 8.08397348]),
  np.array([3.04613769, 0.97672114]),
  np.array([6.84233027, 4.40152494]),
  np.array([1.22038235, 4.9517691 ]),
  np.array([0.34388521, 9.09320402]) ])

p = role_assignment(teammate_positions, formation_positions)
print(p)

