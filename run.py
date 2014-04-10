#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import uuid
from bottle import run, route, request, static_file, redirect

# variables
audio_save_location = os.path.join(os.getcwd(), 'audio')
index_template_file = open(os.path.join(os.getcwd(), 'templates', 'index.html'))
index_template = index_template_file.read()
index_template_file.close()

@route('/')
def index():
	# This is naked HTML, soon to be replaced with good templating... Sorry!
    return index_template

@route("/gen", method='POST')
def genaudio():
    text = request.forms.get('text') or "আমি বাংলায় গান গাই"
    text = unicode(text, 'UTF-8')
    uuid_id = str(uuid.uuid4())
    subprocess.call(['espeak', '-w', os.path.join(audio_save_location, uuid_id + '.wav'), text])
    redirect("/get/" + uuid_id + '.wav')

@route('/get/<path:path>')
def getaudio(path):
    return static_file(path, root=audio_save_location)

run(host='0.0.0.0', port=8080, debug=True)
