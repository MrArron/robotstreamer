import os
import time
import traceback
import ssl
import urllib.request
import getpass
import json



ConfigFilename = "/home/pi/config_" + getpass.getuser() + ".json"

KeepAlivePeriod = 60


def times(lst, number):
        return [x*number for x in lst]


def getWithRetry(url, secure=True):

    for retryNumber in range(2000):
        try:
            print("GET", url)
            if secure:
                object = urllib.request.urlopen(url)

            else:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                object = urllib.request.urlopen(url, context=ctx)



            break
        except:
            print("could not open url", url)
            traceback.print_exc()
            time.sleep(2)

    data = object.read()
    encoding = object.info().get_content_charset('utf-8')
    return data.decode(encoding)



def sendSerialCommand(ser, command):


    print(ser.name)         # check which port was really used
    ser.nonblocking()

    # loop to collect input
    #s = "f"
    #print "string:", s
    print(str(command.lower()))
    ser.write(command.lower() + "\r\n")     # write a string
    #ser.write(s)
    ser.flush()

    #while ser.in_waiting > 0:
    #    print "read:", ser.read()

    #ser.close()



def makePOST(url, data):

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url,
                                 data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    return response


def sendCameraAliveMessage(infoServerProtocol, infoServer, cameraID):

    print("sending camera alive message")
    url = '%s://%s/v1/set_camera_status' % (infoServerProtocol, infoServer)
    print("url", url)
    try:
            response = makePOST(url, {'camera_id': cameraID,
                                      'camera_status':'online'})
    except:
            print("could not make post to", url)
