"""
WSGI entry point for production deployment (Gunicorn / Render / Railway).

Usage:
    gunicorn visualizer.wsgi:server --bind 0.0.0.0:$PORT
"""

import warnings
import os
import sys

warnings.simplefilter(action='ignore', category=FutureWarning)

# Ensure project root is on sys.path
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.insert(0, path2root)

import logging
from dash import dcc, html
from dash.dependencies import Input, Output

from storage.builtin_datasets import ActiveNetwork
from visualizer import app


# --------------------------------------------------------------------------- #
# Logger — write to stderr in production (Render captures it automatically)
# --------------------------------------------------------------------------- #
logger = logging.getLogger("crimenet")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


# --------------------------------------------------------------------------- #
# Layout & routing (same as index.py, but without run_server)
# --------------------------------------------------------------------------- #
app.visualizer_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.visualizer_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        app.active_network = ActiveNetwork(path_2_data=None, from_file=False)
        return app.layout
    else:
        return '404'


# --------------------------------------------------------------------------- #
# Expose the Flask server object for Gunicorn
# --------------------------------------------------------------------------- #
server = app.visualizer_app.server
