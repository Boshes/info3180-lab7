import os
from app import app
from flask import render_template, request, redirect, url_for,jsonify,session,send_file
import json
import time
import requests
import BeautifulSoup
import urlparse

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/thumbnail/process', methods=['POST'])
def get_images():
    json_data = json.loads(request.data)
    print "inside the image thing"
    url = json_data.get('url')
    print url
    images = BeautifulSoup.BeautifulSoup(requests.get(url).text).findAll("img",src=True)
    urllist = []
    for image in images:
        if "sprite" not in image["src"]:
            urllist.append(urlparse.urljoin(url, image["src"]))
    print jsonify(imagelist=urllist)
    return jsonify(imagelist=urllist)