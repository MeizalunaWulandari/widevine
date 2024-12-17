# Import dependencies
from flask import Flask, render_template, request, jsonify, session, redirect, send_file, Response, current_app
import requests
import scripts
import uuid
import json
import base64
from pywidevine import __version__
from pywidevine.pssh import PSSH
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine import RemoteCdm

# Create database if it doesn't exist
scripts.create_database.create_database()

# Check for .WVD file and assign it a variable
WVD = scripts.wvd_check.check_for_wvd()

# If no WVD found, exit
if WVD is None:
    WVD = 'Remote'
    rcdm = RemoteCdm(
                device_type='ANDROID',
                system_id=int(requests.post(url='https://cdrm-project.com/devine').content),
                security_level=3,
                host='https://cdrm-project.com/devine',
                secret='CDRM-Project',
                device_name='CDM'
            )

# Define Flask app object, give template and static arguments.
app = Flask(__name__)

# Create a secret key for logins
app.secret_key = str(uuid.uuid4())

# Route for root '/'
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        # Get the JSON data from the request
        data = json.loads(request.data.decode())

        # Get the proxy
        proxy = data['Proxy']
        if proxy == '':
            proxy = None

        decrypt_response = scripts.decrypt.decrypt_content(
            in_pssh=request.json['PSSH'],
            license_url=request.json['License URL'],
            headers=request.json['Headers'],
            json_data=request.json['JSON'],
            cookies_data=request.json['Cookies'],
            input_data=request.json['Data'],
            wvd=WVD,
            proxy=proxy,
        )
        return jsonify(decrypt_response)

# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run(debug=True)
