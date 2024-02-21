import subprocess
import json
import time
from flask import Flask,jsonify,request
from flask_cors import CORS
import requests

main = Flask(__name__)
CORS(main)

@main.route('/macadd',methods=['POST'])
def macadd():
    data = request.json
    print("Received data : ",data)
    print("Received data mac add : ",data['Mac Address']) #00:10:f3:7d:b8:23
    macaddress = data['Mac Address']
    print("Received data store id : ",data['Store ID']) #se0180vpr001
    storeid = data['Store ID']
    set_loc = ""
    command = f"Set-Location -Path 'C:\\Users\\KAKIA\\Desktop\\SN B\\';cmd /c plink.exe -ssh -batch -t sysaiopsadmin@{storeid} -pw xB59T5ZH 'show user-table | include pos | include {macaddress}'"
    print("command : ",command)
    time.sleep(3)
    result = subprocess.run(["powershell","-Command",command],capture_output=True,text=True)

    if result.returncode == 0:
        print("Output : ",result.stdout)
    else:
        print("Error : ",result.stderr)

    output = result.stdout
    split_output = output.split()
    print("split type : ",type(split_output))
    print("split : ",split_output)

    temp = {
        "id" : 1
    }

    for i in range(len(split_output)):
        temp.update({str(i) : split_output[i]})

    return jsonify({"message":"Script executed succssfully with payload!"},{"mac_data" : temp}),200

@main.route('/connecti',methods=['POST'])
def connecti():
    data = request.json
    print("Received data : ",data)
    print("Received data mac add : ",data['Mac Address']) #00:10:f3:7d:b8:23
    macaddress = data['Mac Address']
    split_string = macaddress.split(':')
    macadd_url = ""
    print(len(split_string))
    for i in range(len(split_string)):
        if(i<len(split_string)-1):
            macadd_url = macadd_url+str(split_string[i])+"%3A"
        if(i==len(split_string)-1):
            macadd_url = macadd_url+split_string[i]

    base_url  = "https://apigw-eucentral2.central.arubanetworks.com/monitoring/v2/clients/"
    url = base_url+macadd_url
    print("url : ",url)

    header = {
        'User-Agent' : 'python-requests',
        'Authorization' : 'Bearer eKDq8TPnkKJ0YUMl28L3pDKyeb0M9AK4',
        'Content-Type': 'application/json'
    }

    export_data=""

    try:
        response = requests.get(url,headers=header,verify=False)
        if response.status_code == 200:
            export_data = response.json()
            print(export_data)
        else:
            print("Error : ",response.status_code)
            export_data = "Error"
    except:
        export_data = "Error"

    return jsonify({"message":"Script executed succssfully with payload!"},{"mac_data" : export_data}),200

@main.route('/switchstatus',methods=['POST'])
def switchstatus():
    data = request.json
    print("Received data : ",data)
    print("Received data mac add : ",data['serial']) 
    serial = data['serial']
    print("serial : ",serial)
    url = f"https://apigw-eucentral2.central.arubanetworks.com/monitoring/v1/switches/{serial}/ports"
    print("url : ",url)

    header = {
        'User-Agent' : 'python-requests',
        'Authorization' : 'Bearer eKDq8TPnkKJ0YUMl28L3pDKyeb0M9AK4',
        'Content-Type': 'application/json'
    }

    export_data=""

    try:
        response = requests.get(url,headers=header,verify=False)
        if response.status_code == 200:
            export_data = response.json()
            print(export_data)
        else:
            print("Error : ",response.status_code)
            export_data = "Error"
    except:
        export_data = "Error"

    return jsonify({"message":"Script executed succssfully with payload!"},{"mac_data" : export_data}),200

if __name__ == '__main__':
    main.run(debug=True)

