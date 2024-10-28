import numpy as np

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


