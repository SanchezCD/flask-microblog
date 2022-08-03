import os
from flask import Flask , render_template , request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()



def create_app():
    app = Flask(__name__)
    client = MongoClient( os.environ.get("MONGODB_URI") )
    app.db = client.microblog


    @app.route('/' , methods = [ "GET" , "POST" ] )
    def home():
        print( [e for e in app.db.entries.find({ })] )
        
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatterd_date = datetime.datetime.today().strftime("%Y-%m-%d")
            
            #entries.append((entry_content , formatterd_date) )
            
            app.db.entries.insert_one({"content":entry_content, "date":formatterd_date } )
            
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b-%d")
            )
            for entry in app.db.entries.find({})
        ]
        
            
        return render_template(
            "home.html", entries = entries_with_date
        )

    return app
