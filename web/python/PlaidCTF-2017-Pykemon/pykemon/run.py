from flask import Flask, request, session, render_template, render_template_string
from random import randint
from pykemon import *
import json
import os
import re


app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'XXXXXXXXX'


class PageTemplate(object):
    def __init__(self, template):
        self.template = template

@app.route('/')
def index():
    r = Room()
    balls = 10
    session['room'] = r.__dict__ 
    session['caught'] = {'pykemon': list()}
    session['balls'] = balls
    for pykemon in r.pykemon:
        print pykemon

    print session['caught']
    return render_template('index.html', pykemon=r.pykemon, balls=balls)
    

@app.route('/catch/', methods=['POST'])
def pcatch():
    name = request.form['name']
    if not name:
        return 'Error'
    
    balls = session.get('balls')
    balls -= 1
    if balls < 0:
        return "GAME OVER"
    
    session['balls'] = balls
    p = check(name, 'room')
    
    if not p:
        return "Error: trying to catch a pykemon that doesn't exist"
    
    r = session.get('room')
    for pykemon in r['pykemon']:
        if pykemon['pid'] == name:
            r['pykemon'].remove(pykemon)
            print pykemon, r['pykemon']
    
    session['room'] = r

    s = session.get('caught')
    
    if p.rarity > 90:
        s['pykemon'].append(p.__dict__)
        session['caught'] = s
        if r['pykemon']:
            return p.name + ' has been caught!' + str(balls)
        else:
            return p.name + ' has been caught!' + str(balls) + '!GAME OVER!'
    
    elif p.rarity > 0:
        chance = (randint(1,90) + p.rarity) / 100
        if chance > 0:
            s['pykemon'].append(p.__dict__)
            session['caught'] = s
            if r['pykemon']:
                return p.name + ' has been caught!' + str(balls)
            else:
                return p.name + ' has been caught!' + str(balls) + '!GAME OVER!'
    if r['pykemon']:
        return p.name + ' got away!'+ str(balls)
    else:
        return p.name + ' got away!'+ str(balls) + '!GAME OVER!'

@app.route('/rename/', methods=['POST'])
def rename():
    name = request.form['name']
    new_name = request.form['new_name']
    if not name:
        return 'Error'

    p = check(name, 'caught')
    if not p:
        return "Error: trying to name a pykemon you haven't caught!"
    
    r = session.get('room')   
    s = session.get('caught')
    for pykemon in s['pykemon']:
        if pykemon['pid'] == name:
            pykemon['nickname'] = new_name
            session['caught'] = s
            print session['caught']
            return "Successfully renamed to:\n" + new_name.format(p)
    
    return "Error: something went wrong"

def check(name, prop):
    s = session.get(prop)
    if 'pykemon' in s.keys():
        for pykemon in s['pykemon']:
            if pykemon['pid'] == name:
                return Pykemon(pykemon['name'], pykemon['hp'])
    return None

@app.route('/buy/', methods=['POST'])
def buy():
    balls = session.get('balls') + 1
    if balls < 0:
        return "GAME OVER"

    session['balls'] = balls
    return str(balls)

@app.route('/caught/', methods=['POST'])
def caught():
    pykemons = session.get('caught')
    print pykemons
    if len(pykemons['pykemon']):
        result = "<ul>"
        for p in pykemons['pykemon']:
            result += "<img src="+p['sprite']+" width=32px height=32px><strong>"+p['nickname']+"</strong>: "+p['description']+"<br/>"
        result += "</ul>"
        return result
    return "You have not caught any Pykemons"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
