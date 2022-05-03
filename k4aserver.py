# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time,sys
import base64
from utils.cams import ir_preprocess, cam_initialize, modify_contrast_and_brightness

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'localhost'#  socket.gethostbyname(host_name)
print(host_ip)
port = 8888
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

k4a = cam_initialize()

IR = False
IR = True
# while True:
msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ',client_addr)
WIDTH = 720
HEIGHT = 450
fail_n = 0
frame_n = 0
while True:
    key = cv2.waitKey(1)
    capture = k4a.get_capture()
    if np.any(capture.depth) and capture.color is not None:
        if IR:
            frame = modify_contrast_and_brightness(capture.ir.copy(),a=8.0,b=-250.0)
            frame = ir_preprocess(frame)
        else: frame = capture.color
        image = frame.copy()
        cv2.imshow('Initial', image)

        send_frame = image[:,:,:3].copy()
        print(send_frame.shape)
        if send_frame.shape[1]>=WIDTH:
            send_frame = imutils.resize(image,width=WIDTH)
        cv2.imshow('resize', send_frame)
        encoded,buffer = cv2.imencode('.jpg',send_frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        print('rate: ' + str((frame_n-fail_n)/(frame_n+0.0000000001)),fail_n)
        if sys.getsizeof(message)<=65535:
            print("Send {0} bytes of data.".format(sys.getsizeof(message)))
            server_socket.sendto(message,client_addr)
        else:
            print("Send {0} bytes of data.".format(sys.getsizeof(message)))
            fail_n += 1

        frame_n += 1

    if key == ord('q'):
        break
k4a.stop()
cv2.destroyAllWindows()