from flask import Flask, jsonify, render_template
#import socket

app = Flask(__name__)

def fetchDetails():
    hostname = "Ecosia"
#    hostname =socket.gethostname()
#    ip = socket.gethostbyname(hostname)
    return str(hostname)

@app.route("/")
def Ecosia_GreenTrees():
    return "<p>Welcome to Ecosia, GreenTrees!</p>"

@app.route("/health")
def health():
    return jsonify(
        status="UP"
    )
    
@app.route("/tree")
def tree():
    return jsonify(
        favourite_tree="MANGO"
    )

@app.route("/details")
def details():
    hostname = fetchDetails()
    return render_template('index.html', HOSTNAME=hostname)

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=5003)
=======
    app.run(host='0.0.0.0', port=5000)
>>>>>>> 98b878bf1bb9c8750e8e183260fb23eaec3867a1
