from flask import Flask, render_template, request, redirect
import requests
import json 
import random
import os
import dateutil.parser

app = Flask(__name__)


# Helper function to parse a raw timestamp to a desired format of "H:M:S dd/mm/yyy"
def myChangeFunc(timestamp):
	t = dateutil.parser.parse(timestamp)
	finalT = t.strftime("%H:%M:%S %d/%m/%Y")
	return finalT

# Route: index page
@app.route("/")
@app.route("/index")
def index():
    r = requests.get('http://localhost:3000/api/org.example.biznet.SampleAsset') 
    if r.json()==None or r.json()=={}:
        transactions = {}
    else:
        transactions = r.json()

    return render_template('index.html', transactions = transactions)



# Route: submitPizza transaction
@app.route("/submitPizza", methods=['POST', 'GET'])
def submitPizza():
	state_info = request.form['state'].encode('utf-8').lower()
	if(state_info=="production"):
		json_val = {
			  "$class": "org.acme.howto.Pizza",
			  "pizzaId": "p1zzA",
			  "timestamp": request.form['timestamp'].encode('utf-8'),
			  "date": request.form['date'].encode('utf-8'),
			  "state": request.form['state'].encode('utf-8').lower(),
			  "owner": "factory"
			}	
		transactions_val = {
			  "$class": "org.acme.howto.ChangeStateTo"+state_info.title(),
			  "pizza": "p1zzA"
			}
		# Making 2 POST requests with JSON data as a parameter 
		# POST Request 1: Create a new Pizza element with its respective fields 
		r = requests.post('http://localhost:3000/api/Pizza', data=json_val)
		# POST Request 2: Issue a ChangeStateToProduction transaction
		rT = requests.post('http://localhost:3000/api/ChangeStateTo'+state_info.title(), data=transactions_val)
	else:
		json_val = {
			  "$class": "org.acme.howto.Pizza",
			  "pizzaId": "p1zzA",
			  "timestamp": request.form['timestamp'].encode('utf-8'),
			  "date": request.form['date'].encode('utf-8'),
			  "state": request.form['state'].encode('utf-8').lower(),
			  "owner": "factory"
			}	
		transactions_val = {
			  "$class": "org.acme.howto.ChangeStateTo"+state_info.title(),
			  "pizza": "p1zzA"
			}
		# Making 1 POST request with JSON data as a parameter
		# POST Request: Issue a ChangeStateTo<state>; where <state> is the state selected from the dropdown
		rT = requests.post('http://localhost:3000/api/ChangeStateTo'+state_info.title(), data=transactions_val)
	# return("The status code of the POST/PUT is: "+ str(rT.status_code) + " , " + str(rT.text))
	return redirect("/factory")

# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 5000))

# Entry point to the program
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
