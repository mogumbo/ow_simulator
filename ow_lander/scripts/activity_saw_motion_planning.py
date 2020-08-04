#!/usr/bin/env python

# __BEGIN_LICENSE__
# Copyright (c) 2018-2019, United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration. All
# rights reserved.
# __END_LICENSE__

import constants
import math
import copy
from tf.transformations import quaternion_from_euler
from utils import is_shou_yaw_goal_in_range
from activity_full_digging_traj import plan_cartesian_path_lin
from activity_full_digging_traj import move_to_pre_trench_configuration
from activity_full_digging_traj import go_to_Z_coordinate, change_joint_value


def saw_motion_planning(move_arm, move_limbs, x_tr, y_tr, depth, length):

  pre_move_complete = move_to_pre_trench_configuration(move_arm, x_tr, y_tr)
  if pre_move_complete == False:
    return False

  # rotate hand
  change_joint_value(move_arm,constants.J_HAND_YAW, -2*math.pi/3)

  # approaching and entering terrain - along -Z
  z_tr = constants.GROUND_POSITION + 3*constants.SCOOP_HEIGHT - depth
  go_to_Z_coordinate(move_limbs,x_tr,y_tr,z_tr)

  # sawing ice - along +X
  cartesian_plan, fraction = plan_cartesian_path_lin(move_arm, length)
  move_limbs.execute(cartesian_plan, wait=True)
  move_limbs.stop()

  # exiting terrain - along +Z
  z_tr = constants.GROUND_POSITION + constants.SAW_OFFSET - depth
  go_to_Z_coordinate(move_arm,x_tr,y_tr,z_tr)


  return True