import math
import numpy as np
from math_ops.Math_Ops import Math_Ops as M



class Strategy():
    def __init__(self, world):
        self.play_mode = world.play_mode
        self.robot_model = world.robot  
        self.my_head_pos_2d = self.robot_model.loc_head_position[:2]
        self.player_unum = self.robot_model.unum
        self.mypos = (world.teammates[self.player_unum-1].state_abs_pos[0],world.teammates[self.player_unum-1].state_abs_pos[1])
       
        self.side = 1
        if world.team_side_is_left:
            self.side = 0

        self.teammate_positions = [teammate.state_abs_pos[:2] if teammate.state_abs_pos is not None 
                                    else None
                                    for teammate in world.teammates
                                    ]
        
        self.opponent_positions = [opponent.state_abs_pos[:2] if opponent.state_abs_pos is not None 
                                    else None
                                    for opponent in world.opponents
                                    ]



        

        self.team_dist_to_ball = None
        self.team_dist_to_oppGoal = None
        self.opp_dist_to_ball = None

        self.prev_important_positions_and_values = None
        self.curr_important_positions_and_values = None
        self.point_preferences = None
        self.combined_threat_and_definedPositions = None


        self.my_ori = self.robot_model.imu_torso_orientation
        self.ball_2d = world.ball_abs_pos[:2]
        self.ball_vec = self.ball_2d - self.my_head_pos_2d
        self.ball_dir = M.vector_angle(self.ball_vec)
        self.ball_dist = np.linalg.norm(self.ball_vec)
        self.ball_sq_dist = self.ball_dist * self.ball_dist # for faster comparisons
        self.ball_speed = np.linalg.norm(world.get_ball_abs_vel(6)[:2])
        
        self.goal_dir = M.target_abs_angle(self.ball_2d,(15.05,0))

        self.PM_GROUP = world.play_mode_group

        self.slow_ball_pos = world.get_predicted_ball_pos(0.5) # predicted future 2D ball position when ball speed <= 0.5 m/s

        # list of squared distances between teammates (including self) and slow ball (sq distance is set to 1000 in some conditions)
        self.teammates_ball_sq_dist = [np.sum((p.state_abs_pos[:2] - self.slow_ball_pos) ** 2)  # squared distance between teammate and ball
                                  if p.state_last_update != 0 and (world.time_local_ms - p.state_last_update <= 360 or p.is_self) and not p.state_fallen
                                  else 1000 # force large distance if teammate does not exist, or its state info is not recent (360 ms), or it has fallen
                                  for p in world.teammates ]

        # list of squared distances between opponents and slow ball (sq distance is set to 1000 in some conditions)
        self.opponents_ball_sq_dist = [np.sum((p.state_abs_pos[:2] - self.slow_ball_pos) ** 2)  # squared distance between teammate and ball
                                  if p.state_last_update != 0 and world.time_local_ms - p.state_last_update <= 360 and not p.state_fallen
                                  else 1000 # force large distance if opponent does not exist, or its state info is not recent (360 ms), or it has fallen
                                  for p in world.opponents ]

        self.min_teammate_ball_sq_dist = min(self.teammates_ball_sq_dist)
        self.min_teammate_ball_dist = math.sqrt(self.min_teammate_ball_sq_dist)   # distance between ball and closest teammate
        self.min_opponent_ball_dist = math.sqrt(min(self.opponents_ball_sq_dist)) # distance between ball and closest opponent

        self.active_player_unum = self.teammates_ball_sq_dist.index(self.min_teammate_ball_sq_dist) + 1

        self.my_desired_position = self.mypos
        self.my_desired_orientation = self.ball_dir


    def GenerateTeamToTargetDistanceArray(self, target, world):
        for teammate in world.teammates:
            pass
        

    def IsFormationReady(self, point_preferences):
        
        is_formation_ready = True
        for i in range(1, 12):
            if i != self.active_player_unum: 
                teammate_pos = self.teammate_positions[i-1]

                if not teammate_pos is None:

                    distance = np.sum((teammate_pos - point_preferences[i]) **2)
                    if(distance > 0.3):
                        is_formation_ready = False

        return is_formation_ready

    def GetDirectionRelativeToMyPositionAndTarget(self,target):
        target_vec = target - self.my_head_pos_2d
        target_dir = M.vector_angle(target_vec)

        return target_dir
    

    def lineOfSight(self, target):
        x0 = self.mypos[0]
        x1 = target[0]
        y0 = self.mypos[1]
        y1 = target[1]
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            for opp in self.opponent_positions:
                if opp is not None:
                    if x0-1.5 <= opp[0] <= x0+1.5  and  y0-1.5 <= opp[1] <= y0+1.5:
                        return False
            
            if sx == 1:
                if sy == 1:
                    if x0 >= x1 and y0 >= y1:
                        break
                else:
                    if x0 >= x1 and y0 <= y1:
                        break
            else:
                if sy == 1:
                    if x0 <= x1 and y0 >= y1:
                        break
                else:
                    if x0 <= x1 and y0 <= y1:
                        break

            e2 = 2*err
            if e2 >= -dy:
                err -= dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return True
    
    def teamInBox(self):
        teammates = self.teammate_positions
        for i in range(len(teammates)):
            if i != self.player_unum-1:
                if teammates[i][0] >= 10 and (-4 <= teammates[i][1] <= 4):
                    return True
        return False
    
    def pass_reciever_selector(self, player_unum, teammate_positions, final_target):
        goalDist = np.linalg.norm(self.slow_ball_pos-np.array(final_target))
        if goalDist <= 5 and self.lineOfSight(final_target):
            currTarget = final_target
        elif 5 < goalDist < 8 and self.lineOfSight((12, 0)) and self.teamInBox():
            currTarget = (12, 0)
        else:
            options = []
            for i in range(len(teammate_positions)):
                if i != player_unum-1 and teammate_positions[i] is not None:
                    if self.lineOfSight(teammate_positions[i]):
                        if np.linalg.norm(self.slow_ball_pos-np.array(teammate_positions[i])) < 8:
                            options.append(teammate_positions[i])

            if not options:
                if -15 < teammate_positions[player_unum-1][0] < 15:
                    newX = teammate_positions[player_unum-1][0]+0.5
                else:
                    newX = teammate_positions[player_unum-1][0]
                if teammate_positions[player_unum-1][1] <= 0:
                    newY = teammate_positions[player_unum-1][1]+0.5
                else:
                    newY = teammate_positions[player_unum-1][1]-0.5

                currTarget = [newX, newY]
            else:
                currTarget = options[0]
                currX = float('-inf')
                for pos in options:
                    if pos[0] > currX:
                        currTarget = pos
                        currX = pos[0]
        
        target = currTarget

        return target

