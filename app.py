# import eel
from main import *
from flask import Flask, jsonify
from flask_cors import CORS
import json

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
# eel.init('app', allowed_extensions=['.js', '.html'])

# # FL1 = []
# # FL2 = []
# # BL1 = []
# # BL2 = []
# # BENCH = ['Taric', 'Sion', 'None', 'None', 'None', 'None', 'Samira', 'Samira', 'Tristana']

# # BOARD = [
# #     'None', 'None', 'None', 'None', 'Vex', 'Yuumi', 'None', # FL1 'first prediction', 'second prediction', 'first prediction'.....
# #     'None', 'None', 'Taric', 'None', 'None', 'None', 'None', # FL2
# #     'None', 'None', 'None', 'Talon', 'None', 'Janna', 'None', # BL1
# #     'Malzahar', 'None', 'Viktor', 'None', 'Lulu', 'None', 'Lux' # BL2
# #     ]

# @eel.expose                         # Expose this function to Javascript
# def scan():
#     window_capture()
#     first_predictions, second_predictions = process_board()
#     return [first_predictions, second_predictions]

# #eel.say_hello_js('Python World!')   # Call a Javascript function

# eel.start('index.html', mode='edge')             # Start (this blocks and enters loop)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/board', methods=['GET'])
def scan():
    window_capture()
    first_predictions, second_predictions = process_board()
    return json.dumps([first_predictions, second_predictions])


if __name__ == '__main__':
    app.run()