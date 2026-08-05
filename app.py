from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "FortiCNAPP Demo"

@app.route("/ping")
def ping():

    host = request.args.get("host")

    output = subprocess.check_output(
        "ping -c 1 " + host,
        shell=True
    )

    return output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
