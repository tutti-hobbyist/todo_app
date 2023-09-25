#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from app.models.model import Request
from app.models.database import db_session
from datetime import datetime

#Flaskオブジェクトの生成
app = Flask(__name__)

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")

#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index")
def index():
    name = request.args.get("name")
    requests = Request.query.all()
    return render_template("index.html",name=name,requests=requests)

# POSTリクエストを受け取る機構
@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    requests = Request.query.all()
    return render_template("index.html", name=name, requests=requests)

# フォームの値を受け取ってINSERT処理をする
@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = Request(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()

# UPDATE処理
@app.route("/update",methods=["post"])
def update():
    content = Request.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return index()

# DELETE処理
@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = Request.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return index()

#おまじない
if __name__ == "__main__":
    app.run(debug=True)