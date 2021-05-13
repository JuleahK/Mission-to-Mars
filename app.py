#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# In[8]:


app = Flask(__name__)


# In[9]:


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# In[10]:


@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


# In[11]:


@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)


# In[ ]:


if __name__ == "__main__":
   app.run()


# In[ ]:




