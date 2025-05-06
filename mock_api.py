from flask import Flask, send_file

app = Flask(__name__)

@app.route('/', methods=['GET'])
def send_dummy_file():
    try:
        return send_file("dummy_transcript.txt")
    except FileNotFoundError:
        return {"error": "dummy_transcript.txt not found"}, 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
