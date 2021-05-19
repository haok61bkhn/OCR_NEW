from Textdetection import Text_detector
from Vocr import OCR
import cv2
import pickle
from preprocess_ocr import Preprocess_OCR

text_detector=Text_detector()
ocr=OCR()
preprocess_ocr=Preprocess_OCR()

image_origin = cv2.imread("data/uyquyen.png")

# cv2.imshow("image_origin",img)
img,det_imgs,dt_boxes=text_detector.detect(image_origin.copy())
cv2.imwrite("data/image.jpg",img)

boxes_noises=preprocess_ocr.get_box_red_word(image_origin.copy())

dt_boxes,det_imgs=preprocess_ocr.remove_boxes(boxes_noises, dt_boxes,det_imgs)



list_texts=[]
d=0
for det_img in det_imgs:
    cv2.imwrite("output/"+str(d)+".jpg",det_img)
    list_texts.append(ocr.predict(det_img))
    d+=1
    # cv2.imshow("image",det_img)
    # cv2.waitKey(0)
pickle.dump((dt_boxes,list_texts),open("res.pickle","wb+"))

