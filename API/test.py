from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        parms = request.get_json(force=True)
        print(parms['city'])
        return jsonify({'parms':parms['city']})

    # elif request.method == 'GET':
    #     tmp1 = request.args.get('name', 'user01')
    #     tmp2 = request.args.get('juso', 'hellow')
    #     return jsonify({'name':tmp1, 'jsuo':tmp2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


"""
app 실행 명령어:
FLASK_ENV=development FLASK_APP=API/test.py flask run

송신할 때:
import request
requests.post("http://127.0.0.1:5000/predict", json={'city':'seoul'}).text

.text => 내부 데이터 받기 위해서 사용(이 옵션 사용안하면 response 결과값만 반환)
"""