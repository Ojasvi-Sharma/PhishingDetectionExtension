import flask
from flask import Flask, request, render_template, jsonify
from sklearn.externals import joblib
import numpy as np
import impFuncs
import json

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')



@app.route('/predict2', methods=['POST'])
def make_prediction():

	if request.method=='POST':

		url = request.form['url']

		subdomains = impFuncs.checkSubdomains(url)
		ssl = impFuncs.checkSSL(url)
		if ssl[1] == -1 or ssl[1] == '-1':
			sslf = input('Enter ssl cert check value manually: ')
		else:
			sslf = ssl[1]
		hasHTTPS = impFuncs.checkHTTPSinURL(url)
		anchors = impFuncs.checkAnchors(url)
		if anchors == 'Nope':
			anchors = input('Enter the value for Anchor manually: ')
			anchors = (int(anchors) - 215.22)/90.4 
		svform = impFuncs.checkServerForm(url)
		if svform == 'Nope':
			svform = input('Enter the value for Forms manually: ')
		prefSux = impFuncs.prefixSuffix(url)

		print("Subdomain: ",subdomains, "presuf: ",prefSux, "anchor: ", anchors, "Forms: ", svform, "SSL: ", sslf, "hasHTTPS: ",hasHTTPS)

		prediction = model.predict([[subdomains, prefSux, anchors, svform, sslf, hasHTTPS]])

		label = str(np.squeeze(prediction))

		if label == 'no':
			prd = 'URL is Safe'
		else:
			prd = 'URL is Not Safe'

		print("Prediction: "+label)

		d = {'res':prd}

		return json.dumps(d)
		
		#return render_template('index.html', label=label)

if __name__ == '__main__':

	model = joblib.load('classifier3.pkl')
	app.run(host='0.0.0.0', port=8000, debug=True)