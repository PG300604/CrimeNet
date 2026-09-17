import warnings
import os
import sys

# suppress warning caused by panda
# once this is dealt with in the analyzer module, remove following
warnings.simplefilter(action='ignore', category=FutureWarning)

# APPEND PATH TO ROOT TO ENSURE INTERNAL IMPORTS
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.append(path2root)

import logging
from logging.handlers import RotatingFileHandler

from dash import dcc, html
from dash.dependencies import Input, Output

from storage.builtin_datasets import ActiveNetwork
from visualizer import app


# ------------------------------------------------------------------------------------ #


# SET UP LOGGER
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler('visualizer.log', backupCount=1)
handler.setFormatter(formatter)
handler.setLevel('DEBUG')
logger.addHandler(handler)


# INITIAL LAYOUT
app.visualizer_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# CALLBACK ROUTING '/'
@app.visualizer_app.callback(Output('page-content', 'children'),
                             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        app.active_network = ActiveNetwork(path_2_data=None, from_file=False)
        return app.layout
    else:
        return '404'


# ------------------------------------------------------------------------------------ #


# PARSE ARGUMENTS, ADD EXTERNAL DATASETS AND LOGGER, RUN SERVER
if __name__ == '__main__':
    app.visualizer_app.server.logger.addHandler(handler)
    app_host='0.0.0.0'
    if app.args.host:
        app_host=str(app.args.host)
    if app.args.debug:
        app.visualizer_app.run_server(host=app_host, debug=True)
    else:
        app.visualizer_app.run_server(host=app_host, debug=False)
