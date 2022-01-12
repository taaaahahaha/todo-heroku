import pymongo
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://taaham:123@cluster0.imuxc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Todo"]


username = "Data"
collection = db[username]

data_obj = collection.find({})

print(data_obj)

for i in data_obj:
    print(i)












# collection = db["Data"]


# # Collection for storing UserID-Passwords
# collection_uid = db["Userid-passwords"]

# # collection_uid.insert_one(
# #                         {
# #                             "username":"username1",
# #                             "email":"email1",
# #                             "password":"password1"
# #                         }
# #                     )

# results = collection_uid.find_one({'username':"username1"})

# print(results["password"])

