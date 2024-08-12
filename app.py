from flask import Flask, jsonify, request
from browser import search_facebook_marketplace


app = Flask(__name__)
app.secret_key = "testops-monitoring-sp-xha4234-!ksoadko-daskoef34ko3"


@app.route("/status")
def get_status():
    return jsonify(status="ok")


@app.route("/start-triger", methods=["POST","GET"])
def start_triger():
    try:
        data = request.get_json()
        location = data['location']
        search   = data['search']
        search_facebook_marketplace(location,search)
        return jsonify(status="complate")
    except Exception as error:
        return jsonify(status="error", Error=str(error)), 502
    


if __name__ == "__main__":  
    #app.run(host="0.0.0.0", port=3000, ssl_context='adhoc', threaded=True)
    app.run(host="0.0.0.0", port=3000, debug=False, threaded=True)