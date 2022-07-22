# this module will be imported in the into your flowgraph

an1=-90
an2=90
angle = an1

step = 1

def sweeper(prob_lvl) : 
    global an1,an2,angle, step
    if prob_lvl :
        angle += step

    if angle > an2 :
        angle = an1

    return angle