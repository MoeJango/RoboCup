import numpy as np

def zerosCovered(costArr, coveredArr):
    for i in range(11):
        for j in range(11):
            if costArr[i][j] == 0 and not coveredArr[i][j] == 1:
                return False
    return True


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
                coveredArr[:, j] = 1
                break

    while(not zerosCovered(costArr, coveredArr)):
        for i in range(11):
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
                        path = np.zeros((11, 11))
                        path[i][j] = 1
                        done = False
                        while (not done):
                            
                        
                        
                        
        
            


    # Example
    point_preferences = {}
    for i in range(1, 12):
        point_preferences[i] = formation_positions[i-1]


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
