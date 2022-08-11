from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
from id import create_id
client = MongoClient("본인 url추가")
db = client.Fanbook

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/fanbook", methods=["POST"])
def fanbook_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]
    id = create_id()

    doc = {
        'id' : id,
        'name': name_receive,
        'comment': comment_receive,
        'likes': 0
    }

    db.fanbook.insert_one(doc)
    return jsonify({'msg':'응원 완료!'})

@app.route("/fanbook/likes", methods=["POST"])
def fanbook_likes():
    id_receive = request.form["id_give"]
    likes_count = db.fanbook.find_one({'id': int(id_receive)})['likes'] + 1
    db.fanbook.update_one({'id': int(id_receive)}, {'$set': {'likes': likes_count}})
    return jsonify({'likes': likes_count})

@app.route("/fanbook/del", methods=["POST"])
def fanbook_del():
    id_receive = request.form["id_give"]
    db.fanbook.delete_one({'id': int(id_receive)})

    return jsonify({'msg': '응원을 삭제 합니다.'})

@app.route("/fanbook", methods=["GET"])
def fanbook_get():
    fanbook_list = list(db.fanbook.find({},{'_id':False}))
    return jsonify({'fanbook':fanbook_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
