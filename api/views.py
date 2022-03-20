from api import api_blue
from flask import *
import requests, json
import time




@api_blue.route('/', methods=['GET'])
def Bing():
    return 'OK'