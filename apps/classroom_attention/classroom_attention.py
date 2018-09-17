# Face tracking, people counting

import numpy as np
import cv2
import time
import collections
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(1)
PERCENT_MOVEMENT       = 2.1
TRACK_IT               = 10
show_frame             = True
show_marks             = True

nfaces_data = collections.deque(maxlen=TRACK_IT*2)
nsmiles_data = collections.deque(maxlen=TRACK_IT*2)

def expand_area(x,y,w,h):
    new_w = int(w*PERCENT_MOVEMENT)
    new_h = int(h*PERCENT_MOVEMENT)
    new_x = int(x-((new_w-w)/2))
    if new_x <0:
        new_x = 0
    new_y = int(y-((new_h-h)/2))
    if new_y <0:
        new_y = 0
    return new_x, new_y, new_w, new_h

def get_circ_coord(x,y,w,h):
    return (x+w/2),(y+h/2), (max(w/2, h/2))

def find_new_centroid(olist, frame):
    new_list=[]
    for i, (x, y, w, h) in enumerate(olist):
        nx, ny, nw, nh = expand_area(x,y,w,h)
        faces=faces_detection(frame[ny:ny+nh, nx:nx+nw])
        if len(faces)>=1:
            [dx, dy, dw, dh] = faces[0]
            new_list.append([dx+nx, dy+ny, dw, dh])
    return new_list

def faces_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    return faces

def write_text_on_image(frame, nfaces, nsmiles, max_people):
    text='Gente detectada: {}'.format(max_people)
    cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,125,255),2)
    text='Gente contentos: {}'.format(nsmiles)
    cv2.putText(frame,text,(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,125,255),2)
    text='Gente atenta: {}'.format(nfaces)
    cv2.putText(frame,text,(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,125,255),2)

def draw_on_image(frame, coord_list):
    if show_marks==True:
        for i, (x,y,w,h) in enumerate(coord_list):
            cv2.circle(frame,(x+w/2,y+h/2), max(w/2,h/2), (0,0,255), 3)
            cv2.putText(frame,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,100,255),1)

def check_smile(frame, faces):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nsmiles = 0
    for i, (x,y,w,h) in enumerate(faces):
        print ("w={}, h={}".format(w,h))
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor= 1.2,minNeighbors=5,minSize=(12, 12))
        if len(smiles)!=None:
            nsmiles+=1
        if show_marks==True:
            for (ex,ey,ew,eh) in smiles:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
    return nsmiles

def update_face_list(new_faces, old_faces):
    for i, (nx,ny,nw,nh) in enumerate(new_faces):
        ncx, ncy, nra = get_circ_coord(nx,ny,nw,nh)
        on_list = False
        for v, (ox, oy, ow, oh) in enumerate(old_faces):
            ocx, ocy, ora = get_circ_coord(ox,oy,ow,oh)
            center_distance = ((ocx-ncx)**2+(ocy-ncy)**2)**(0.5)
            if ((center_distance+nra)<PERCENT_MOVEMENT*ora):
                old_faces[v]=[nx,ny,nw,nh]
                on_list=True
                break
        if on_list==False:
            old_faces.append([nx,ny,nw,nh])
    return old_faces

def anime_show_data(nfaces, nsmiles):
    line_faces.set_ydata(nfaces)  # update the data
    line_happy.set_ydata(nhappy)  # update the data
    return line_faces, line_happy


state = 'detection'
track_face_list = []
max_people = 0

while(True):
    ret, frame = cap.read()
    # frame = cv2.imread('im3.jpg')
    start = time.time()
    if state=='detection':
        new_detection_faces=faces_detection(frame)
        track_face_list = update_face_list(new_detection_faces, track_face_list)
        state = 'tracking'
        track_time = TRACK_IT
    else: 
        if state=='tracking':
            track_face_list=find_new_centroid(track_face_list, frame)
            track_time-=1
            if track_time==0:
                state = 'detection'
    end = time.time()

    # Collect data
    nsmiles_data.append(check_smile(frame, track_face_list))
    nfaces_data.append(len(track_face_list))

    # Filter data
    nsmiles = int(np.median(nsmiles_data))
    nfaces  = int(np.median(nfaces_data))

    if track_time ==0:
        if max_people<nfaces:
            max_people = nfaces

    draw_on_image(frame, track_face_list)
    write_text_on_image(frame,nfaces,nsmiles, max_people)
        
    # Display the resulting frame
    if show_frame==True:
        cv2.imshow('frame',frame)
    # sys.stdout.write("Time: %fsec, Gente: %d, Contentos: %d, Maximo: %d   \r" % (end-start, nfaces, nsmiles, max_people) )
    # sys.stdout.flush()
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('m'):
        show_marks = not(show_marks)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
