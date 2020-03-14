################################################################
### Author : Micah Vandersteen | Date : 11 March 2020
### This code is meant to use MongoDB alongside Flask to create
### a new HTML page that displays all of the information that 
### was scraped in the 'mission_to_mars.ipynb' file.
################################################################

# importing dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# instantiating Flask app
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it if it does not exist
db = client.mars_db

# creating '/scrape' route
@app.route('/scrape')
def scrape():
    
    # scraping data
    mars_scrape_data = scrape_mars.scrape()

    # Update Mongo database 
    db.mars_info_coll.update({}, mars_scrape_data, upsert = True)
    
    # getting data
    mars_data = db.mars_info_coll.find_one()
    
    # Redirect back to home page display
    return redirect("/", code = 302)

# creating homepage route
@app.route('/')
def index():

    # Return template and data
    return render_template("index.html", mars_data = mars_data)


if __name__ == "__main__":
    app.run(debug = True)
