from flask import Flask
from flask import render_template
from flask import Response

import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen():
	while True:
	    success, frame = camera.read()

	    if not success:
	    	
	        frame = cv2.imencode('.jpg', img)[1].tobytes()
	        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	    else:
	        break

@app.route('/video_feed')
def video_feed():
	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)