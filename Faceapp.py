from flask import Flask, render_template, Response, request
from VideoStream import VideoStream
from FaceFilters import FaceFilters
from faceTk import GUIFace
import time

filters = ['glasses.png', 'eyes.png','eyelasses.png','3dglasses.png', 'swag.png', 'cat.png', \
        'monkey.png', 'rabbit.png','moustache.png', 'moustache1.png', 'ironman.png','spiderman.png','batman.png', 'capAmerica.png',]
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
	if request.method == "POST":
                vs = VideoStream(0).start()
                fc = FaceFilters(filters)
                time.sleep(2.0)
                gui = GUIFace(vs,fc,'output')
        return render_template('index.html')

if __name__ == '__main__':

        
        app.run(debug=True)