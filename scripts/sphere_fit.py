#!/usr/bin/env python3
import rospy
import numpy as np

def main():
	#define node subscribers and publishers
	rospy.init_node('sphere_fit', anonymous = True)
	# define subscriber
	xyzarray = rospy.Subscriber('robot_vision_lectures/SphereParams', xc, yc, zc)
	
	print(xyzarray)



if __name__ == '__main__':
	main()
