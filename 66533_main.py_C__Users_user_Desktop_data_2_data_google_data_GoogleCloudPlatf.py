# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

from flask import Flask, render_template
from flask_sockets import Sockets
import requests


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
sockets = Sockets(app)


# [START metadata]
METADATA_NETWORK_INTERFACE_URL = \
    ('http://metadata/computeMetadata/v1/instance/network-interfaces/0/'
     'access-configs/0/external-ip')


def get_external_ip():
    """Gets the instance's external IP address from the Compute Engine metadata
    server. If the metadata server is unavailable, it assumes that the
    application is running locally.
    """
    try:
        r = requests.get(
            METADATA_NETWORK_INTERFACE_URL,
            headers={'Metadata-Flavor': 'Google'},
            timeout=2)
        return r.text
    except requests.RequestException:
        logging.info('Metadata server could not be reached, assuming local.')
        return 'localhost'
# [END metadata]


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def index():
    # Websocket connections must be made directly to this instance, so the
    # external IP address of this instance is needed.
    external_ip = get_external_ip()
    return render_template('index.html', external_ip=external_ip)
# [END app]


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error ocurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    print("""
This can not be run directly because the Flask development server does not
support web sockets. Instead, use gunicorn:

gunicorn -b 127.0.0.1:8080 -b 127.0.0.1:65080 -k flask_sockets.worker main:app

""")
