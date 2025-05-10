from flask import Flask, render_template
from redis import Redis
import json

app = Flask(__name__)
redis_client = Redis(host='localhost', port=6379, db=0)

@app.route("/")
def index():
    anomaly_logs_raw = redis_client.lrange("anomaly_logs", 0, -1)
    anomaly_logs = [json.loads(log.decode('utf-8')) for log in anomaly_logs_raw]
    return render_template("index.html", logs=anomaly_logs)

if __name__ == "__main__":
    app.run(debug=True)