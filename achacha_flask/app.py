from flask import Flask


# flask 기본 포트 : 5000

app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'

app.run()
# already in use 일 경우, port=5001
# flask가 자동으로 꺼졌다가 다시 실행되도록 하는 코드는 debug=True (상용화에서는 사용 금지)