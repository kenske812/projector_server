# coding: utf-8


"""Tests projector server.
First, run the server by "python projector_server.py".
By running this program, 2 images are thrown to the server.

Returns:
    [type] -- [description]
"""

import json
import urllib.request
import numpy as np
import time

def cosine(x, y):
    return (0.5*np.cos(x) + 0.5) * (0.5*np.cos(y) + 0.5)

def create_fringe(n, m, freqx, freqy=0, phase_x=0, phase_y=0):
    """[summary]
    
    Arguments:
        n {[int]} -- # of rows
        m {[int]} -- # of cols
        freqx {[float]} -- freqency in horizontal direction
        freqy {[float]} -- freqency in vertical direction   
        phases_x {[list]} -- a list of phases in degree.
        phases_y {[list]} -- a list of phases in degree. if None, all zero.
    
    Returns:
        [list] -- 2d numpy arrays. (max, min) for output wave are (1, 0)
    """


    _x = 2 * np.pi * freqx * np.linspace(0, 1, m)
    _y = 2 * np.pi * freqy * np.linspace(0, 1, n)
    
    x = _x + phase_x
    y = _y + phase_y

    xx, yy = np.meshgrid(x, y)
    zz = cosine(xx, yy)
    return zz


url = "http://localhost:8081"

data1 = {
    "filename": r"C:\Users\kenske\Documents\programs\projector_server\img1.npy",
    "timeout": 5000, #[ms]
}

data2 = {
    "filename": r"C:\Users\kenske\Documents\programs\projector_server\img2.npy",
    "timeout": 1000,
}
headers = {
    'Content-Type': 'application/json',
}

img1 = create_fringe(1200, 1920, 3)
img2 = np.copy(img1)
img2[:500] = 0
np.save(data1["filename"], img1)
np.save(data2["filename"], img2)



req1 = urllib.request.Request(url, json.dumps(data1).encode(), headers)
req2 = urllib.request.Request(url, json.dumps(data2).encode(), headers)


for req in [req1, req2]:
    with urllib.request.urlopen(req) as res:
        print(res.status)
        print(res.msg)
        print(res.read())
        time.sleep(1)