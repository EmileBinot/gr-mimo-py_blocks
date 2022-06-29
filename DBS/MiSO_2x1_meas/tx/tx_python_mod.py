# this module will be imported in the into your flowgraph

from locale import ABMON_1
from termios import FF1


an1=-180
an2=180
angle = an1

step = 1

def sweeper(prob_lvl) : 
    global an1,an2,angle, step
    if prob_lvl :
        angle += step

    if angle > an2 :
        angle = an1

    return angle