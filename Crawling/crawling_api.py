from flask import Flask, request
import run
app = Flask(__name__)
n = 0

@app.route('/', methods=['GET'])
def crawling():
    global n
    if request.method == 'GET':
        n += run.loop()

        if n > 100:
            print("over 100")
            n = 0
        else:
            print("under 100")

    return {'result':n}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
