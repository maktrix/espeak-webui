#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import uuid
from bottle import run, route, request, static_file, redirect, SimpleTemplate

# variables
audio_save_location = os.path.join(os.getcwd(), 'audio')

# templates
index_template_file = open(os.path.join(os.getcwd(), 'templates', 'index.html'))
index_template = index_template_file.read()
index_template_file.close()

player_template_file = open(os.path.join(os.getcwd(), 'templates', 'play.html'))
player_template = player_template_file.read()
player_template_file.close()

notfound_template_file = open(os.path.join(os.getcwd(), 'templates', '404.html'))
notfound_template = notfound_template_file.read()
notfound_template_file.close()

@route('/')
def index():
    return index_template

@route("/gen", method='POST')
def genaudio():
    text = request.forms.get('text') or "আমি বাংলায় গান গাই"
    sex = request.forms.get('sex') or 'female'
    text = unicode(text, 'UTF-8')
    uuid_id = str(uuid.uuid4())

    if sex == 'male':
    	subprocess.call(['espeak', '-w', os.path.join(audio_save_location, uuid_id + '.wav'), text])
    else:
    	subprocess.call(['espeak', '-v+f3', '-w', os.path.join(audio_save_location, uuid_id + '.wav'), text])

    redirect("/get/" + uuid_id)

@route('/get/<path:path>')
def getplayer(path):
	if os.path.isfile(os.path.join(audio_save_location, path + '.wav')):
		return SimpleTemplate(player_template).render(path=path)
	else:
		return notfound_template


@route('/audio/<path:path>')
def getaudio(path):
    return static_file(path, root=audio_save_location)
    os.unlink(os.path.join(audio_save_location,path))


# make the audio directory if it doesn't exist
if not os.path.exists(audio_save_location):
	os.makedirs(audio_save_location)

run(host='0.0.0.0', port=8080, debug=True)
