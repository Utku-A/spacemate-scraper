from flask import Flask, jsonify
from model.cronjob import scheduler
from model.manuel import manuel_job_execute
import os, log

Agent_List_Scanner = os.environ.setdefault('Agent_List_Scanner', 'Ready')
Agent_Page_Scanner = os.environ.setdefault('Agent_Page_Scanner', 'Ready')
Advent_Page_Scanner = os.environ.setdefault('Advent_Page_Scanner', 'Ready')
Advent_Page_Just_Not_Ok_Scanner = os.environ.setdefault('Advent_Page_Just_Not_Ok_Scanner', 'Ready')

app = Flask(__name__)
app.secret_key = "testops-monitoring-sp-xha4234-!ksoadko-daskoef34ko3"
scheduler.init_app(app)
scheduler.start()


@app.route("/status")
def get_status():
    return jsonify(
        Agent_List_Scanner=os.environ['Agent_List_Scanner'],
        Agent_Page_Scanner=os.environ['Agent_Page_Scanner'],
        Advent_Page_Scanner=os.environ['Advent_Page_Scanner']
    )

@app.route("/manuel-start/<string:execute>")
def manuel_job(execute):
    return manuel_job_execute(execute)


if __name__ == "__main__":  
    #app.run(host="0.0.0.0", port=3000, ssl_context='adhoc', threaded=True)
    app.run(host="0.0.0.0", port=3000, debug=False, threaded=True)