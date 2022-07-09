from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/', methods=['POST'])
def model():
    if request.method == 'POST':
        parms = request.get_json(force=True)
        if parms['request'] == "True":
            os.system("python Models/run.py --mode train")
            print("GO")
        else:
            print("STOP")

        return jsonify({'response':True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
