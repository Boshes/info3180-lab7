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
    soup = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    images = BeautifulSoup.BeautifulSoup(requests.get(url).text).findAll("img")
    print "These are images " + str(images)
    urllist = []
    og_image = (soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        print "This is " + og_image['content']
        urllist.append(urlparse.urljoin(url, og_image['content']))
    thumbnail_spec = soup.find('link', rel='image_src')
    print "This is thumbnail " + str(thumbnail_spec)
    if thumbnail_spec and thumbnail_spec['href']:
        urllist.append(urlparse.urljoin(url, thumbnail_spec['href']))
    for image in images:
        if "sprite" not in image["src"]:
            urllist.append(urlparse.urljoin(url, image["src"]))
    print urllist
    print jsonify(imagelist=urllist)
    return jsonify(imagelist=urllist)