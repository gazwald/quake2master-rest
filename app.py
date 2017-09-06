#!/usr/bin/env python3
import json

from database.orm import Server, Status

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


def build_serverlist(game='q2'):
    engine = create_engine('postgresql://q2master:password@192.168.124.86:5432/q2master')
    Session = sessionmaker(bind=engine)
    s = Session()

    str_fmt = '%Y-%m-%d %H:%M'

    serverlist = []
    for server in s.query(Status).join(Server).filter(Server.active == True).all():
        first_seen = server.server.first_seen
        last_seen = server.server.last_seen
        serverdict = server.__dict__
        serverdict['server'] = str(serverdict['server'])
        serverdict['gamename'] = str(serverdict['gamename'])
        serverdict['map'] = str(serverdict['map'])
        serverdict['version'] = str(serverdict['version'])
        serverdict['first_seen'] = first_seen.strftime(str_fmt)
        serverdict['last_seen'] = last_seen.strftime(str_fmt)
        serverdict['_sa_instance_state'] = None
        serverlist.append(serverdict)
    s.close()
    return serverlist

app = Flask(__name__)
CORS(app)
 
@app.route("/<game>/servers")
def servers(game):
    return jsonify(build_serverlist(game))
