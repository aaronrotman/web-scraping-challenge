# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# import test
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_mission")
mars_dict = {
    'latest_news': {'title': '', 'para': ''},
    'feat_image_url': "#",
    'fact_table': "",
    'weather': '',
    'hemisphere_img_urls': '#'
}
# Update the Mongo database using update and upsert=True
mongo.db.collection.update({}, mars_dict, upsert=True)

@app.route("/")
def index():
    
    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    return render_template("index.html", data=destination_data)

@app.route("/scrape")
def scraper():
     # Run the scrape function
    mars_dict = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_dict, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
