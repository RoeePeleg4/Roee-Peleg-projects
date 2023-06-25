import cv2 , time
from PIL import Image
import plivo
import socket
import time

camera = cv2.VideoCapture(0)


def serverConnction():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    ADDR = (HOST , PORT)
    FORMAT = 'utf-8'
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.bind(ADDR)

    s.connect(ADDR)
    print ("[CONNECTED]")
    message = "Detect Enemy"
    s.sendall(message.encode(FORMAT))

    '''with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((HOST , PORT))
        s.sendall(message.encode(FORMAT))
'''

'''def sendSms(senderNumber , destNumber):
    client = plivo.RestClient('<auth_id>' , '<auth_token>')
    response = client.messages.create(
        src=f'{senderNumber}',
        dst=f'{destNumber}',
        text='SomeBody has inveded your room!!!!!!'
    )
    print (response)'''
    
def cuptureTemplate():
    result , image = camera.read()
    time.sleep(1)
    if result:
        cv2.imwrite('photos/firstImage.png' , image)
    cv2.destroyAllWindows() 

def imageCupture():
    result , image1 = camera.read()
    time.sleep(1)
    result , image2 = camera.read()
    if result:
        #cv2.imshow("imageTest1" , image1)
        #cv2.imshow("imageTest2" , image2)

        cv2.imwrite('photos/imageTest1.png' , image1)
        cv2.imwrite('photos/imageTest2.png' , image2)
    #cv2.waitKey(0)
    cv2.destroyAllWindows() 

def video_capture():
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))

    size = (frame_width , frame_height)

    result = cv2.VideoWriter('video/videoOfMovement.avi',cv2.VideoWriter_fourcc(*'MJPG'),30, size)
    local_time = time.time()
    while True:
        ret, frame = camera.read()
        if ret == True: 
            result.write(frame)
            current_time = time.time()
            if current_time-local_time >= 10:
                break
        else:
            break
    camera.release()
    result.release()
    cv2.destroyAllWindows()


    '''ret, frame = camera.read()
    while True:
        ret , frame = camera.read()
        if ret==True:
            cv2.imshow("koolac" , frame)
            key = cv2.waitKey(1)
            if key==ord("q"):
                break
    camera.release()
    cv2.destroyAllWindows()'''

def isSame(list1 , list2):
    if (len(list1) == len(list2)):
        '''counter = 0
        for i in range (len(list1)):
            if list1[i]==list2[i]:
                counter+=1
        print(counter/len(list1))'''

        amount_of_same = sum(1 for pixel1, pixel2 in zip(list1,list2) if pixel1 == pixel2)
        perentege_same = amount_of_same/len(list1)
        return perentege_same
    else:
        raise Exception("images size are not the same")  
    
def compareTwoImages(image1 , image2):
    imageCupture()
    image1 = cv2.cvtColor(cv2.imread(f'photos/{image1}'), cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(cv2.imread(f'photos/{image2}'), cv2.COLOR_BGR2GRAY)
    ssim_score = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)[0][0]
    print (ssim_score)
    if (ssim_score >=0.9):
        return True
    return False
    '''
    percentage = isSame(pix_val1 , pix_val2)
    if percentage>0.4:
        print ("same")
    else:
        print("diffrent")
    '''

def main():
    cuptureTemplate()
    while True:
        print (compareTwoImages("imageTest1.png" , "imageTest2.png") , compareTwoImages("firstImage.png" , "imageTest2.png") , compareTwoImages("imageTest1.png" , "firstImage.png"))
        if (compareTwoImages("imageTest1.png" , "imageTest2.png")==False  or compareTwoImages("imageTest1.png" , "firstImage.png")==False or compareTwoImages("imageTest2.png" , "firstImage.png")==False):
            print("ENEMY HAS INVEDED")
            video_capture()
            serverConnction()
            break;
        time.sleep(1)
        
        



if __name__=="__main__":
    main()
