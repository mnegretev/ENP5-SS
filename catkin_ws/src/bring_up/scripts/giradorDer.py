#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def girador():
	print("Initializing simple move node ...") 
	rospy.init_node('girador', anonymous=True)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
 	loop = rospy.Rate(10)

 	while not rospy.is_shutdown():
 		cmd_vel = Twist()
 		cmd_vel.angular.z = -0.5
 		pub.publish(cmd_vel) 
 		loop.sleep()

if __name__ == '__main__':
	try:
		girador()
	except rospy.ROSInterruptException:
		pass