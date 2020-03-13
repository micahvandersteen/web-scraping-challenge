################################################################
### Author : Micah Vandersteen | Date : 11 March 2020
### This code is meant to use MongoDB alongside Flask to create
### a new HTML page that displays all of the information that 
### was scraped in the 'mission_to_mars.ipynb' file.
################################################################

#Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

#Store the return value in Mongo as a Python dictionary.



#Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.


#Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the #appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your # own design.

# importing dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# instantiating Flask app
app = Flask(__name__)

# establishing connection to MongoDB via PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# creating homepage
@app.route('/')
def home():
    
    # Find one record of data from the mongo database
    #destination_data = mongo.db.collection.find_one()

    # Return template and data
    #return render_template("index.html", vacation=destination_data)


# creating '/scrape' route
@app.route('/scrape')
def scrape():
    
    mars_info = scrape_mars.scrape_info()

    # Update Mongo database 
    mongo.db.collection.update({}, mars_info, upsert = True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)
