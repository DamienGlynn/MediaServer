import os
from flask import Flask, request, render_template

image_dir = 'static/image'
music_dir = 'static/music'
video_dir = 'static/video'


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
	return render_template("index.html")

###############################################################################
# Images

@app.route('/images')
def images():
	files = [f for f in os.listdir(image_dir)]
	files_number = len(files)
	return render_template("images.html",
						   title = 'Images',
						   files_number = files_number,
						   files = files)

@app.route('/image/<filename>')
def image(filename):
    return render_template('image.html', title=filename, file=filename)

###############################################################################
# Music

@app.route('/songs')
def songs():
	files = [f for f in os.listdir(music_dir)]
	files_number = len(files)
	return render_template("songs.html",
						   title = 'Music',
						   files_number = files_number,
						   files = files)

@app.route('/song/<filename>')
def song(filename):
    return render_template('song.html', title=filename, file=filename)


###############################################################################
# Videos

@app.route('/videos')
def videos():
	files = [f for f in os.listdir(video_dir)]
	files_number = len(files)
	return render_template("videos.html",
						   title = 'Videos',
						   files_number = files_number,
						   files = files)

@app.route('/video/<filename>')
def video(filename):
    return render_template('video.html', title=filename, video_file=filename)

###############################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)