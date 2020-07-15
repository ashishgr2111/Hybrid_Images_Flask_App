from flask import Flask, request, render_template, redirect, url_for
import requests, os, time
from main import channel

app = Flask(__name__)

def loadImage(filename, r):
	with open(filename, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=128):
			fd.write(chunk)

@app.route("/", methods=['GET', 'POST'])
def index():
	maxi = 0
	for fol in os.listdir('./static/'):
		maxi = max(maxi, int(fol[3:]))

	if request.method == "POST":
		name1 = request.form["name1"]
		name2 = request.form["name2"]
		r1 = requests.get(name1)
		r2 = requests.get(name2)
		
		maxi += 1
		folder = './static/res' + str(maxi) + '/'
		os.mkdir(folder)
		loadImage(folder + 'image1.jpeg', r1)	
		loadImage(folder + 'image2.jpeg', r2)	
		channel(folder)
		return {
			'image1': "static/res" + str(maxi) + "/image1.jpeg",
			'image2':  "static/res" + str(maxi) + "/image2.jpeg",
			'hybrid': "static/res" + str(maxi) + "/hybrid.jpeg",	
			'current_set': maxi
		}
		
	args = {
		'image1': "../static/res" + str(maxi) + "/image1.jpeg",
		'image2':  "../static/res" + str(maxi) + "/image2.jpeg",
		'hybrid': "../static/res" + str(maxi) + "/hybrid.jpeg",
	}	

	return render_template("index.html", args = args, current_set = maxi)