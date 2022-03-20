from home import home_blue
from flask import *
import requests, json


@home_blue.route('/', methods=['GET'])
def Home():
    return 'Hi'