# © Taaha Multani @ https://github.com/taaaahahaha

# Imports for WebApp
from flask import *
from datetime import datetime

# Imports for MongoDb Database
import pymongo
from pymongo import MongoClient

app = Flask(__name__,template_folder='template',static_folder='static')

# Temporary Cluster
cluster = MongoClient("mongodb+srv://taaham:123@cluster0.imuxc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Todo"]
# collection = db["Data"]
global collection
global username_global


# Collection for storing UserID-Passwords
collection_uid = db["Userid-passwords"]







@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])

        results = collection_uid.find_one({'username':username})
        if results == None:
            flash("Wrong Userid")
            return render_template('signin.html')

        elif results["password"] != password:
            flash("Wrong Password")
            return render_template('signin.html')
        
        else:
            # Individual collection for each usrname
            global collection
            global username_global

            username_global = username
            collection = db[username]

            return redirect('/'+username)

    
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        results = collection_uid.find_one({'username':username})
        if results == None:
            collection_uid.insert_one(
                        {
                            "username":username,
                            "email":email,
                            "password":password
                        }
            )
            db.create_collection(username)
            return render_template('signin.html')
        
        else:
            flash("Username is Already Taken")
            return render_template('signup.html')
    

    return render_template('signup.html')





@app.route('/<usr>', methods=['GET', 'POST'])
def hello_world(usr):
    usr = str(usr)

    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']

        count = collection.count_documents({})

        while True:
            try:
                collection.insert_one(
                        {
                            "_id":count+1,
                            "title":title,
                            "desc":desc,
                            "date_created":datetime.utcnow()
                        }
                    )
                
                break
            except:
                count+=1

        
        
    data_obj = collection.find({})
    return render_template('index.html', allTodo=data_obj, len=collection.count_documents({}), user = usr)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    global collection
    global username_global
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = collection.update_one({"_id":sno},{"$set":{"title":title,"desc":desc}})
        
        return redirect("/"+username_global)
        
    todo = collection.find_one({"_id":sno})
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    global collection
    global username_global
    
    collection.delete_one({"_id":sno})

    return redirect("/"+username_global)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.secret_key = "somesecretkey" 
    app.run(debug=True)