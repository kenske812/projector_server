# coding-utf8

"""

Multiprocess is based on this example:
https://gist.github.com/fspot/5727795

Returns:
    [type] -- [description]
"""

from bottle import Bottle
from bottle import route, run
from bottle import post, request
from bottle import HTTPResponse
import json
import traceback

from pathlib import Path
import numpy as np
from screen_control import Screen

from multiprocessing import Process, Queue, cpu_count
import time


app = Bottle()
app.queue = Queue()
app.nb_workers = cpu_count()

def project_img(filename, timeout):
    """file path(.npy) that is scaled from 0 to 1
    
    Arguments:
        filename {Path} -- Path of .npy. it should be scaled from 0 to 1.
    """
    screen = Screen(1)
    img = np.load(filename)
    
    print("starting " + str(filename))
    screen.show(img, timeout)
    print("end " + str(filename))
    


def pull_jobs(queue):
    while True:
        filename, timeout = queue.get()
        if filename is None:
            break
        
        project_img(Path(filename), timeout)

def write_to_file(d):
    with open("tmp.json", 'w') as f:
        f.write(json.dumps(d, indent=4))


screen_process = Process(name="sp", target=project_img)

@app.post("/")
def project():

    #write_to_file(request.json)
    filename = request.json["filename"]
    timeout = request.json["timeout"]
    app.queue.put((filename, timeout))
    #screen_process = multiprocessing.Process(name="sp", target=project_img, 
    #                                                        args=(filename,))



@app.route('/test')
def index():
    return "projector server is working"

@app.route('/exit')
def end(msg):
    for i in range(app.nb_workers):
        app.queue.put(None)


#run(app, host="localhost", port=8081, debug=True, reloader=True)
def main():
    for i in range(app.nb_workers):
        msg_puller_process = Process(target=pull_jobs, args=[app.queue])
        msg_puller_process.start()

    run(app, host='localhost', port=8081)

if __name__ == "__main__":
    main()