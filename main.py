from flask import Flask,render_template,request,redirect,url_for,flash
import requests
import json
import base64

grant_type = 'xxx'
client_id = 'xxxxxx'
client_secret = 'xxxxx'
username = 'xxx@abc.com'
password = 'xxxx'

get_access_token = 'https://login.salesforce.com/services/oauth2/token?grant_type=' + grant_type + '&client_id=' + client_id + '&client_secret=' + client_secret + '&username=' + username + '&password=' + password

r = requests.post(get_access_token)
json_data = r.json()

access_token = json_data['access_token']

api_url = 'https://ssssdwdw-dev-ed.my.salesforce.com/services/apexrest/v1/accounts'

headers_dict = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json",
                     "Accept": "application/json"}


app = Flask(__name__)
app.secret_key = "Secret Key"

@app.route('/')
def Index():
    return render_template("form.html")

# Post Request for Saving Data
@app.route('/SaveData',methods = ['POST'])
def Save():
    if request.method == 'POST':
        Accname = request.form['accname']
        AccNum = request.form['accnumber']
        AccPhone = request.form['accphone']
        file = request.files.getlist('file')
        print("file ", file)
        attach = []
        for x in file:
            dict = {
                "Body" : base64.b64encode(x.read()).decode('utf-8'),
                "Name" : x.filename
            }
            attach.append(dict)


        string = {
            "thisAccount": {
                "Name": Accname,
                "phone": AccPhone,
                "AccountNumber": AccNum
            },
            "attachments":
                attach
        }
        print('string ',string)
        string = json.dumps(string)


        res = requests.post(api_url, data=string, headers=headers_dict)
        print('Account Successfully Created ',res.text)
        flash("Data Sucessfully Saved")

        return redirect(url_for('Index'))


# Get Request for Retrieving Data

@app.route('/View',methods = ['GET'])
def View():
    if request.method == 'GET':
        res = requests.get(api_url,headers=headers_dict)
        json_data = res.json()

        array = json_data["accountId"]
        print(array)

        for i in array:
            id = i["Id"]  # Getting all the account id's in Salesforce
        return render_template("form.html",array=array)

if __name__  == "__main__":
    app.run(debug=True)