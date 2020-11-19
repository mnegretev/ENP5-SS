from flask import Flask
import rospy
import threading
from geometry_msgs.msg import Twist
app = Flask(__name__)

index_html=open("index.html","r").read()
threading.Thread(target=lambda: rospy.init_node('web_node', disable_signals=True)).start()
pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

@app.route('/')
def hello_world():
    return index_html

@app.route('/left')
def move_left():
    cmd_vel = Twist()
    cmd_vel.angular.z = 0.5
    pub_cmd_vel.publish(cmd_vel)
    return "Moving robot forward"

@app.route('/right')
def move_right():
    cmd_vel = Twist()
    cmd_vel.angular.z = -0.5
    pub_cmd_vel.publish(cmd_vel)
    return "Moving robot forward"

@app.route('/up')
def move_up():
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.5
    pub_cmd_vel.publish(cmd_vel)
    return "Moving robot forward"

@app.route('/down')
def move_down():
    cmd_vel = Twist()
    cmd_vel.linear.x = -0.5
    pub_cmd_vel.publish(cmd_vel)
    return "Moving robot forward"

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
