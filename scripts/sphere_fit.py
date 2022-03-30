#!/usr/bin/env python3
import rospy
import numpy as np
# import msgs
from robot_vision_lectures.msg import XYZarray
from robot_vision_lectures.msg import SphereParams


points_received = False
def get_points(pc):
	# two global arrays for the A and B matricies
	global A
	global B
	global points_received
	A = []
	B = []
	# create a usable variable from the XYZarray that has each x y z value
	p = pc.points
	# iterate through each group of XYZ values
	for i in p:
		# put them into the A and B arrays following lecture slides
		B.append([i.x**2 + i.y**2 + i.z**2])
		A.append([2*i.x, 2*i.y, 2*i.z, 1])
	# convert to numpy arrays
	A = np.array(A)
	B = np.array(B)
	# reshape the arrays into matrix format
	A = np.matrix(A)
	B = np.matrix(B)
	points_received = True
	
	
def main():
	#define node, subscribers and publishers
	rospy.init_node('sphere_fit', anonymous = True)
	# define subscriber
	pointcloud = rospy.Subscriber('/xyz_cropped_ball', XYZarray, get_points)
	# define publisher
	params_pub = rospy.Publisher('/sphere_params', SphereParams, queue_size = 1)
	# set the loop frequency
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		if points_received:
			# calculate the fit using linalg module
			P = np.linalg.lstsq(A, B, rcond=None)
			# get the XYZ points out of the array
			xc = P[0][0]
			yc = P[0][1]
			zc = P[0][2]
			# calculate the radius
			r = np.sqrt(P[0][3] + xc**2 + yc**2 + zc**2)
			# for some reason creating a variable for the parameters addes a random empty element at the end when you try to use the variable in the publisher
			#params = (xc.item(0), yc.item(0), zc.item(0), r.item(0)
			
			# publish the sphere fit parameters
			# .item(0) on each of the items pulls the value out of the matrix object they are in
			params_pub.publish(xc.item(0), yc.item(0), zc.item(0), r.item(0))
		rate.sleep()


if __name__ == '__main__':
	main()
