from flask import *



app = Flask(__name__)
app.secret_key = 'C-i7tyW8~gmckBT'



from home import home_blue
app.register_blueprint(home_blue)

from auth import auth_blue
app.register_blueprint(auth_blue)

from api import api_blue
app.register_blueprint(api_blue)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)