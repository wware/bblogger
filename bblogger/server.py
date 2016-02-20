import logging
import socket
import yaml
from flask import Flask, request

config = yaml.load(open('conf.yml').read())

# Stifle most of the output from Werkzeug.
logging.getLogger('werkzeug').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)

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
    logger.info('%s [%s] %s', client, channel, request.form.get('data'))
    return '', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)    # pragma: no cover
