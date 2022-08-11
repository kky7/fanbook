from pymongo import MongoClient

client = MongoClient("mongodb+srv://test:sparta@cluster0.mndqybx.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.Fanbook

max_id_ls = list(db.max_id.find({},{'_id':False}))
if not max_id_ls:
    cur_max_id = 0
    db.max_id.insert_one({'cur_max_id': 0})
else:
    cur_max_id = max_id_ls[0]['cur_max_id']
    # print('cur_max_id:',cur_max_id)

def create_id():
    global cur_max_id
    db.max_id.update_one({'cur_max_id': cur_max_id}, {'$set':{'cur_max_id': cur_max_id + 1}})
    cur_max_id += 1
    return cur_max_id