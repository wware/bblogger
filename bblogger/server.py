import logging
import socket
import time
import yaml
from flask import Flask, request

config = yaml.load(open('conf.yml').read())
# Stifle most Werkzeug output.
logging.getLogger('werkzeug').setLevel(logging.ERROR)
app = Flask(__name__, static_url_path="")


@app.route("/enabled/<channel>")
def enabled(channel):
    level = 10000
    try:
        levelname = config[channel]
        level = getattr(logging, levelname)
    except:
        pass
    return str(level), 200


@app.route('/log/<channel>', methods=['POST'])
def post(channel):
    client = socket.gethostbyaddr(request.remote_addr)[0]
    print '{0} [{1}:{2}] {3}\n{4}:{5} {6}\n{7}\n'.format(
        client,
        channel,
        request.form['levelname'],
        time.ctime(float(request.form['created'])),
        request.form['pathname'],
        request.form['lineno'],
        request.form['funcName'],
        request.form['msg']
        # exc_info????
    )
    return '', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)    # pragma: no cover
