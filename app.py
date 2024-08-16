from flask import Flask, jsonify, request
from browser import search_facebook_marketplace
from cronjob import scheduler
import os, config


app = Flask(__name__)
app.secret_key = "testops-monitoring-sp-xha4234-!ksoadko-daskoef34ko3"

scheduler.init_app(app)
scheduler.start()

@app.route("/status")
def get_status():
    return jsonify(
        Agent_List_Scanner=os.environ['Agent_List_Scanner'],
        Agent_Page_Scanner=os.environ['Agent_Page_Scanner'],
        Search_Location=os.environ['Search_Location'],
        Search_Query=os.environ['Search_Query']
    )


@app.route("/start-triger/list-page", methods=["POST","GET"])
def start_triger_list_page():
    try:
        data = request.get_json()
        if os.environ['Agent_List_Scanner'] == "Ready":
            os.environ['Search_Location']       = data['location']
            os.environ['Search_Query']          = data['search']
            os.environ['Agent_List_Scanner']    = 'Starter'
            return jsonify(status="ok")
        else: return jsonify(status="Şuan uygun değil"),401
    except Exception as error:
        return jsonify(status="error", Error=str(error)), 502


@app.route("/stop-triger/list-page", methods=["POST","GET"])
def stop_triger_list_page():
    if os.environ['Agent_List_Scanner'] == "Running":
        os.environ['Agent_List_Scanner'] = "Stoped"
        return jsonify(status="ok")
    else: return jsonify(status="Henüz çalışmayan şeyi durduramazsın."),401


@app.route("/start-triger/list-detail", methods=["POST","GET"])
def start_triger_detail_page():
    try:
        if os.environ['Agent_Page_Scanner'] == "Ready":
            os.environ['Agent_Page_Scanner'] = "Starter"
            return jsonify(status="ok")
        else: return jsonify(status="Şuan uygun değil"),401
    except Exception as error:
        return jsonify(status="error", Error=str(error)), 502
    

@app.route("/stop-triger/list-detail", methods=["POST","GET"])
def stop_triger_detail_page():
    if os.environ['Agent_Page_Scanner'] == "Running":
        os.environ['Agent_Page_Scanner'] = "Stoped"
        return jsonify(status="ok")
    else: return jsonify(status="Henüz çalışmayan şeyi durduramazsın."),401


if __name__ == "__main__":  
    #app.run(host="0.0.0.0", port=3000, ssl_context='adhoc', threaded=True)
    app.run(host="0.0.0.0", port=3000, debug=False, threaded=True)