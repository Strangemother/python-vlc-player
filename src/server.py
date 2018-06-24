"""Using flask to expose the main entry point as it makes it easier to
expose an input thread.
Individual threads will boot manually or attached through manual setup
"""
from multiprocessing.dummy import Process, Queue
import flask
from flask import Flask
import time
try:
    import Queue as Q
    from Queue import Empty
except ImportError:
    from queue import Queue, Empty

from flask import render_template
import logging
import simple


logging.basicConfig(level=logging.DEBUG)

def log(*a):
    logging.info(' '.join(map(str, a)))

warn = logging.warn

app = Flask(__name__)
global_prc = None
proc_q = None
standard_config = {}


def thread_run(queue=None, config=None):
    global queue_prc
    global socket_prc

    conf = config or {}
    settings = standard_config.copy()
    settings.update(conf)
    q = queue or Queue()
    global_prc = Process(target=run_core, args=(q, settings))
    global_prc.start()

    return global_prc, q


def run_core(queue, config):
    ''' Run the process '''
    log('run')
    run = 1
    config = config or {}

    # uri = config.get('socket_uri', None)
    # socket = _json_socket(uri)
    # socket.send("run_core")
    # pf.init()
    service = simple.Service()
    while run:
        m = None
        try:
            m = queue.get_nowait()
            log('Got message', m)
        except Empty as e:
            pass

        if m == 'kill':
            log('kill run_core')
            run = 0

        if m is None:
            time.sleep(.1)
            continue

        # Any message to this point came from websocket(through queue) or
        # queue internal
        log('assess', m)
        a = m.get('action', None)
        if a is not None:
            del m['action']
            meth = getattr(service, a)
            log('Calling', a)
            meth(**m)

    log('End run core.')


def main():
    app.run(
        debug=True,
        host='127.0.0.1',
        port=9000,
    )


def proc_start():
    global global_prc
    global proc_q

    if global_prc is not None:
        return global_prc

    options = {}

    global_prc, proc_q = thread_run(proc_q, options)

    return global_prc


def proc_stop():
    global global_prc
    if global_prc is None:
        return True
    proc_q.put_nowait('kill')
    log('sent kill command, waiting for death.')
    global_prc.join()
    log('Stop complete')
    global_prc = None
    return True


@app.route("/")
def index_page():
    proc_start()
    return render_template('index.html')


@app.route("/start")
def start():
    proc_start()
    return "Run main thread!"

import json
from flask import request, Response


@app.route("/request", methods=['POST'])
def json_post():
    data = None


    action = request.form.get('action')
    uri = request.form.get('uri')
    data = dict(action=action, uri=uri)
    success = False
    if proc_q is not None:
        proc_q.put(data)
        success = True

    js = json.dumps({ "success": success, "data": data })

    callmap = dict(
        start_thread=start,
        stop_thread=stop,
    )

    meth = callmap.get(action, None)
    if meth is not None:
        js['accept'] = 'top'
        meth()



    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'localhost'
    # elif request.headers['Content-Type'] == 'application/octet-stream':
    #     f = open('./binary', 'wb')
    #     f.write(request.data)
    #             f.close()
    #     return "Binary message written!"

    # else:
    #     return "415 Unsupported Media Type ;)"
    return resp


@app.route('/put/<data>')
def put_string(data):
    proc_q.put(data)
    return data


@app.route("/stop")
def stop():
    proc_stop()
    return "kill thread"


if __name__ == '__main__':
    main()
