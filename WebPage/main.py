import cv2 as cv
from flask import Flask, render_template, Response
import cv2
import rospy
import threading
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

app = Flask(__name__)

'''index_html=open("index.html","r").read()'''
threading.Thread(target=lambda: rospy.init_node('web_node', disable_signals=True)).start()
pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
image_pub = rospy.Publisher("/camera/color/image_raw", Image, queue_size=1)

camera = cv2.VideoCapture(-1) #webcamara
bridge = CvBridge()

def gen_frames(): 
    while True:
        success, frame = camera.read()  # lee el marco de la camara
        #dtype, n_channels = bridge.encoding_as_cvtype2('8UC3')
        #im = np.ndarray(shape=(480, 640, n_channels), dtype=dtype)
        cv_image = bridge.imgmsg_to_cv2(frame, desired_encoding="passthrough")

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', cv_image)
            cv_image = buffer.tobytes()
            yield (b'--cv_image\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + cv_image + b'\r\n') # concat frame uno por uno y muestra el resultado

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=cv_image')
'''
@app.route('/')
def index():
    return index_html
'''
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

@app.route('/stop')
def not_move():
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.0
    cmd_vel.angular.z = 0.0
    pub_cmd_vel.publish(cmd_vel)
    return "Moving robot forward"

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
