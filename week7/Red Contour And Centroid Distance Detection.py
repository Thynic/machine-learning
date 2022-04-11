"""
9.04.2022

Yangın Alanı Tespiti
"""

import numpy as np
from math import cos, sin, radians, tan
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('orj', frame)
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([160, 100, 0])
    upper = np.array([180, 255, 255])


    # lower_o = np.array([0, 120, 50])
    # upper_o = np.array([20, 255, 255])

    # lower_o = np.array([0, 120, 50])
    # upper_o = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    # mask_orange = cv2.inRange(hsv, lower_o, upper_o)


    result = cv2.bitwise_and(frame, frame, mask=mask)
    #result_orange = cv2.bitwise_and(frame, frame, mask=mask_orange)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 255)

    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.imshow('Canny Edges After Contouring', edged)

    cv2.drawContours(result, contours, -1, (0, 255, 0), 1)

    # Point cloud'ların koordinatları
    lower_red = np.array([0, 220, 0])  # BGR-code of your lowest red
    upper_red = np.array([10, 255, 10])  # BGR-code of your highest red
    mask = cv2.inRange(result, lower_red, upper_red)
    coord = cv2.findNonZero(mask)
    # for i in coord:
    #     print(i)
    # print("###############################################")

    # Seçilen rengin çerçevelenen alanının orta noktası
    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    M = cv2.moments(thresh)
    try:
        noktalar = []
        # j = 0
        theta = np.deg2rad(60)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # Centroid ve Point cloudların en kısa mesafesi
        height, width = result.shape[:2]
        min_ = height**2 + width**2
        xb, yb = 10, 10 #eski 
        j = 0
        for i in coord:
            x, y = i[0] #(2, 3), (5, 4)
            distance = ((cX - x)**2 + (cY - y)**2)**1/2
            distance2 = ((cX - xb)**2 + (cY - yb)**2)**1/2

            if (j != 0) and (cY != yb and cX != xb and cX != x and cY != y): #zerodivision'dan gaçın
                m1 = ((cY - yb) / (cX - xb))
                m2 = ((cY - y) / (cX - x))
                if (m1 != m2) and (m1 != 0 and m2 != 0) and (m1 * m2 != -1): #zerodivision'dan gaçın
                    angle = (m1 - m2) / (1 + (m1 * m2)) #iki doğru arasındaki açının tanjantı
                    if (angle**-1 < 60) and (angle**-1 > 55): #tanjanttan açıyı almak
                        cv2.line(result, (cX, cY), (x, y), (255, 0, 0), 2)
            j += 1

            if min_ > distance:
                min_ = distance
                minX, minY = x, y

            xb = x
            yb = y

        cv2.circle(result, (minX, minY), 5, (255, 255, 255), -1)
        # cv2.line(result, (cX, cY), (minX, minY), (255, 0, 0), 2)
        cv2.putText(result, "point", (minX - 25, minY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.circle(result, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(result, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # orjX, orjY = minX - cX, minY - cY
        
        # # xd, yd = xd + cX, yd + cY
        # m = ((cX - x))
        # for i in coord:
        #     x, y = i[0]
            
        #     if int(y - yd) == int(m * int(x - xd)):
        #         print("Buldu")
        #         cv2.line(result, (cX, cY), (x, y), (255, 0, 0), 2)

    except:
        pass

    cv2.imshow('Contours', result)

    #cv2.imshow('frame', result)
    #cv2.imshow('frame2', result_orange)
    cv2.imshow('mask', mask)
    #cv2.imshow('mask_orange', mask_orange)



    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
