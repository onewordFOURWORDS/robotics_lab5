#!/usr/bin/env python3
import rospy
import numpy as np
# import msgs
from robot_vision_lectures.msg import XYZarray
from robot_vision_lectures.msg import SphereParams

def get_points(pc):
	# two global arrays for the A and B matricies
	global A
	global B
	A = []
	B = []
	# create a usable variable from the XYZarray that has each x y z value
	p = pc.points
	# iterate through each group of XYZ values
	for i in p:
		# put them into the A and B arrays following lecture slides
		A.append([i.x**2 + i.y**2 + i.z**2])
		B.append([2*i.x, 2*i.y, 2*i.z, 1])
	# convert to numpy arrays
	A = np.array(A)
	B = np.array(B)
	# reshape the arrays
	A = A.reshape((-1,3))
	B = B.reshape((-1,1))
	print(A)
	
	
	
def main():
	#define node, subscribers and publishers
	rospy.init_node('sphere_fit', anonymous = True)
	# define subscriber
	pointcloud = rospy.Subscriber('/xyz_cropped_ball', XYZarray, get_points)
	# define publisher
	params_pub = rospy.Publisher('/sphere_params', SphereParams, queue_size = 1)
	# set the loop frequency
	rate = rospy.Rate(10)
	
	
	
	rospy.spin()


if __name__ == '__main__':
	main()
