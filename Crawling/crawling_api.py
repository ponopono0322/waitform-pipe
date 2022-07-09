from flask import Flask, request
import run
app = Flask(__name__)
n = 0

@app.route('/', methods=['GET'])
def crawling():
    global n        # 전체 개수
    is_over = False     # 1000건이 넘는지 검사하는 것
    if request.method == 'GET':
        n += run.loop()     # 크롤링 함수 실행
        is_over = True if n > 1000 else False

    if is_over:
        tmp = n     # 임시변수
        n = 0       # 값 초기화(오버플로우 방지)   
        return {'result':tmp}
    else:
        return {'result':n}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
