import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

#this function activates when a person is authorized
def process_logging():
    import time
    with open("logs.txt", "a") as f:
        f.write(f"{data} - {time.ctime()}\n")
        f.close()

#this function activates when a person is authorized
def process_auth():
    from playsound import playsound
    print(f"Authorized - {data}")
    process_logging()
    playsound("auth.mp3")

#this function activates when a person is unauthorized
def process_unauth():
    from playsound import playsound
    print(f"Unauthorized - {data}")
    playsound("unauth.mp3")

#this process restarts the program
def process_restart():
    import os
    import sys
    print("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':

    #setting capture device and window sizes
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(3,640)
    capture.set(4,480)

    #opens file and reads the file (file handling)
    with open('allowlist.txt') as f:
        lock = f.read()

    #extracting the data from qrcode
    while (True):
        ret, frame = capture.read()
        for qrcode in decode(frame, symbols=[ZBarSymbol.QRCODE]):
            data = qrcode.data.decode("utf-8")
            #verifing scanned data == data on allowlist
            if data in lock:
                #if authourized do this
                cv2.destroyAllWindows()
                process_auth()
                process_restart()
            else:
                #if unauthourized do this
                cv2.destroyAllWindows()
                process_unauth()
                process_restart()

        cv2.imshow('AuthSys Scanning', frame)
        if cv2.waitKey(1) == ord('q'):
            break
