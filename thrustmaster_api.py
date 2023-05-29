#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
from pygame.locals import *
import pygame
import sys
import os
import time

import roslibpy
from multiprocessing import Process
import signal

from simple_joystick import thrusmaster_handle
app = Flask(__name__)
api = Api(app)

thrustmaster_current_state = False
thrusmaster_pid = None




class ThrustmasterGetState(Resource):
    def get(self):
        global thrustmaster_current_state 
        return {'state': thrustmaster_current_state}
        


class ThrustmasterSetState(Resource):
    def get(self, thrustmaster_state):
        global thrustmaster_current_state 
        global thrusmaster_pid
        change = False
        if thrustmaster_state is None:
            return {'error': 'mauvaise route'}
        
        if bool(int(thrustmaster_state)) and not thrustmaster_current_state:
            if thrusmaster_pid is None:
                p = Process(target=thrusmaster_handle, args=('kakiri-robot.local', 9090, 'vesc/cmd_vel',))
                p.start()
                thrusmaster_pid = p.pid
                change =True
                thrustmaster_current_state = bool(int(thrustmaster_state))
                #print('process.pid of the processus function', pid)
                #print('os.getpid() of the main function', os.getpid())
        if not bool(int(thrustmaster_state)) and thrustmaster_current_state:
            if thrusmaster_pid is not None:
                os.kill(thrusmaster_pid, signal.SIGKILL)
                thrusmaster_pid = None
                change =True
                thrustmaster_current_state = bool(int(thrustmaster_state))
        return {'change': change, 'state': thrustmaster_current_state}

        

api.add_resource(ThrustmasterGetState, '/api/thrustmaster/get_state') # Route_1
api.add_resource(ThrustmasterSetState, '/api/thrustmaster/set_state/<thrustmaster_state>') # Route_2


if __name__ == '__main__':
    app.run(port='5002', debug=False)
