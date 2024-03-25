from flask import Flask, render_template, Response, request
import cv2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('take_photo.html')

vs = None

def gen():
    global vs
    while True:
        ret, frame = vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/take_photo', methods=['POST'])
def take_photo():
    global vs
    file_path = 'filePath'
    success, frame = vs.read()
    if success:
        cv2.imwrite(file_path, frame)
        if os.path.exists(file_path):
            return "success", 200
    return "failed", 500

@app.route('/video_feed')
def video_feed():
    global vs
    vs = cv2.VideoCapture(0)
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='raspberryIP', port=9090, debug=True, threaded=True)
