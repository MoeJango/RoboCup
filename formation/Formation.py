import numpy as np
from math import sin, cos, sqrt

def GenerateBasicFormation():

    formation = [
        np.array([-13, 0]),    # Goalkeeper
        np.array([-10, -2]),  # Left Defender
        np.array([-11, 3]),   # Center Back Left
        np.array([-8, 0]),    # Center Back Right
        np.array([-3, 0]),   # Right Defender
        np.array([0, 1]),    # Left Midfielder
        np.array([2, 0]),    # Center Midfielder Left
        np.array([3, 3]),     # Center Midfielder Right
        np.array([8, 0]),     # Right Midfielder
        np.array([9, 1]),    # Forward Left
        np.array([12, 0])      # Forward Right
    ]

    return formation

def BuildUpFirst():
    formation = [
        np.array([-13, 0]),    # Goalkeeper
        np.array([-12, -4.5]),  # Left Defender
        np.array([-12, 3]),   # Center Back Left
        np.array([-8, -6]),    # Center Back Right
        np.array([-7, 7]),   # Right Defender
        np.array([-5, 9]),    # Left Midfielder
        np.array([-4, 0]),    # Center Midfielder Left
        np.array([-1, 3]),     # Center Midfielder Right
        np.array([1, 7]),     # Right Midfielder
        np.array([3, 1]),    # Forward Left
        np.array([2, -4])      # Forward Right
    ]
    return formation

def BuildUpSecond():
    formation = [
        np.array([-13, 0]),    # Goalkeeper
        np.array([-12, -4]),  # Left Defender
        np.array([-12, 4]),   # Center Back Left
        np.array([-7, 7]),    # Center Back Right
        np.array([-7, -7]),   # Right Defender
        np.array([-4, 2]),    # Left Midfielder
        np.array([-3, -4]),    # Center Midfielder Left
        np.array([1, 0]),     # Center Midfielder Right
        np.array([6, -1]),     # Right Midfielder
        np.array([5, -8]),    # Forward Left
        np.array([7, 6])      # Forward Right
    ]
    return formation

def BuildUpLast():
    formation = [
        np.array([-13, 0]),    # Goalkeeper
        np.array([-8, -4]),  # Left Defender
        np.array([-8, 4]),   # Center Back Left
        np.array([-2, 7]),    # Center Back Right
        np.array([-2, -7]),   # Right Defender
        np.array([0, 3]),    # Left Midfielder
        np.array([3, -4]),    # Center Midfielder Left
        np.array([5, 0]),     # Center Midfielder Right
        np.array([9, -1]),     # Right Midfielder
        np.array([12, -8]),    # Forward Left
        np.array([10, 6])      # Forward Right
    ]
    return formation


def lowBlock(opponents, ballPos, ballDir, myGoalDir):
    formation = [np.array([-14, 0])]
    formation.append(ballPos)
    blockingPosX = ballPos[0] + sqrt(2)*cos(myGoalDir)
    blockingPosY = ballPos[1] + sqrt(2)*sin(myGoalDir)
    formation.append(np.array([blockingPosX, blockingPosY]))  
    for opp in opponents:
        if opp[0] <= -5 and not (ballPos[0]-1.5 < opp[0] < ballPos[0]+1.5 and ballPos[1]-1.5 < opp[1] < ballPos[1]+1.5):
            formation.append(np.array(opp))
        if len(formation) == 11:
            break
    i = 0
    while len(formation) < 11:
        if i == 0:
            target = np.array([-12, -4.5])
        if i == 1:
            target = np.array([-12, 3])
        if i == 2:
            target = np.array([-4, 0])
        if i == 3:
            target = np.array([-8, -6])
        if i == 4:
            target = np.array([-7, 7])
        if i == 5:
            target = np.array([-5, 9])
        if i == 6:
            target = np.array([-1, 3])
        if i == 7:
            target = np.array([1, 5])
        i +=1

        formation.append(target)
    
    return formation


def midBlock(opponents, ballPos, ballDir, myGoalDir):
    formation = [np.array([-14, 0])]
    formation.append(ballPos)
    blockingPosX = ballPos[0] + sqrt(2)*cos(myGoalDir)
    blockingPosY = ballPos[1] + sqrt(2)*sin(myGoalDir)
    formation.append(np.array([blockingPosX, blockingPosY]))  
    for opp in opponents:
        if -7 <= opp[0] <= 5 and not (ballPos[0]-1.5 < opp[0] < ballPos[0]+1.5 and ballPos[1]-1.5 < opp[1] < ballPos[1]+1.5):
            formation.append(np.array(opp))
        if len(formation) == 7:
            break
    i = 0
    while len(formation) < 11:
        if i == 0:
            target = np.array([-12, -4])
        if i == 1:
            target = np.array([-12, 4])
        if i == 2:
            target = np.array([-7, 7])
        if i == 3:
            target = np.array([-4, 2])
        if i == 4:
            target = np.array([-7, -7])
        if i == 5:
            target = np.array([-3, -4])
        if i == 6:
            target = np.array([1, 0])
        if i == 7:
            target = np.array([6, -1])
        i +=1

        formation.append(target)
    
    return formation


def highBlock(opponents, ballPos, ballDir, myGoalDir):
    formation = [np.array([-14, 0])]
    formation.append(ballPos)
    blockingPosX = ballPos[0] + sqrt(2)*cos(myGoalDir)
    blockingPosY = ballPos[1] + sqrt(2)*sin(myGoalDir)
    formation.append(np.array([blockingPosX, blockingPosY]))  
    for opp in opponents:
        if 5 <= opp[0] <= 12 and not (ballPos[0]-1.5 < opp[0] < ballPos[0]+1.5 and ballPos[1]-1.5 < opp[1] < ballPos[1]+1.5):
            formation.append(np.array(opp))
        if len(formation) == 5:
            break
    i = 0
    while len(formation) < 11:
        if i == 0:
            target = np.array([-9, -4])
        if i == 1:
            target = np.array([-9, 4])
        if i == 2:
            target = np.array([0, 3])
        if i == 3:
            target = np.array([-2, 7])
        if i == 4:
            target = np.array([-2, -7])
        if i == 5:
            target = np.array([3, -4])
        if i == 6:
            target = np.array([1, 0])
        if i == 7:
            target = np.array([5, 0])
        i +=1

        formation.append(target)
    
    return formation