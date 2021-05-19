
#Remove word_red
import numpy as np
import cv2
from Textdetection import Text_detector
import pickle
from shapely.geometry import Polygon
class Preprocess_OCR:
    def __init__(self,min_iou=0.5,percent_height=0.6,lower = np.array([130,80,100]),upper = np.array([190,255,255])):
        self.lower=lower
        self.upper = upper
        self.percent_height=percent_height
        self.text_detector=Text_detector()
        self.min_iou=min_iou
        
    def get_red_region(self,image):
        img_or=image.copy()
        result = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([130,80,30])
        upper = np.array([190,255,255])
        mask = cv2.inRange(image, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        # img2 = np.zeros_like(image)
        # print(img2.shape)
        # for i in range(mask.shape[0]):
        #     for j in range(mask.shape[1]):
        #         if(mask[i][j]!=0):
        #             img_or[i][j][0]=255
        #             img_or[i][j][1]=255
        #             img_or[i][j][2]=255

        # cv2.imwrite('mask.jpg', img_or)
        # cv2.imwrite('result.jpg', mask)
        # # cv2.waitKey()

        # img2 = np.zeros_like(img_or)
        # img2[:,:,0] = mask
        # img2[:,:,1] = mask
        # img2[:,:,2] = mask

        return mask,result
    
    def get_box_red_word(self,img):
        mask,result=self.get_red_region(img)
        color = (0, 255, 0)
        print(mask.shape)
        image,det_imgs,dt_boxes=self.text_detector.detect(result)
        h,w=image.shape[:2]
        d=0
       
        list_boxes=[]
        # print(len(dt_boxes))
        for boxes in dt_boxes:
            x_center=int(sum(boxes[:,0])/4)
            y_center=int(sum(boxes[:,1])/4)
            
            if(y_center>self.percent_height*h):
                # print(y_center)
                list_boxes.append(boxes)
        
                image = cv2.line(image, (int(boxes[0][0]),int(boxes[0][1])), (int(boxes[1][0]),int(boxes[1][1])), color, 1) 
                image = cv2.line(image, (int(boxes[1][0]),int(boxes[1][1])), (int(boxes[2][0]),int(boxes[2][1])), color, 1) 
                image = cv2.line(image, (int(boxes[2][0]),int(boxes[2][1])), (int(boxes[3][0]),int(boxes[3][1])), color, 1)
                image = cv2.line(image, (int(boxes[3][0]),int(boxes[3][1])), (int(boxes[0][0]),int(boxes[0][1])), color, 1)
        cv2.imwrite("red_word.jpg",image)
        return list_boxes
    
    def remove_boxes(self,boxes_noises,dt_boxes,det_imgs):
        list_id_removes=[]
        for id_noise,boxes_noise in enumerate(boxes_noises):
            b = Polygon([ (boxes[0],boxes[1])for boxes in boxes_noise])
            max_iou=0
            id_max=0
            for id,dt_box in enumerate(dt_boxes):
                a = Polygon([ (boxes[0],boxes[1])for boxes in dt_box])
                iou=b.intersection(a).area / b.union(a).area
                if(iou>max_iou):
                    max_iou=iou
                    id_max=id
            print("id noise : ",id_noise," ---- id_boxes : ",id_max, "  max_iou: ",max_iou)
            if(max_iou>self.min_iou):
                list_id_removes.append(id_max)
        list_id_removes.sort()
    
        for i in range(len(list_id_removes)-1,-1,-1):
            del dt_boxes[list_id_removes[i]]
            del det_imgs[list_id_removes[i]]
        return dt_boxes,det_imgs


if __name__=="__main__":
    X=Preprocess_OCR()
    img=cv2.imread("data/a.png")
    boxes=X.get_box_red_word(img)
    pickle.dump(boxes,open("boxes_red.pickle","wb+"))





# cv2.imwrite('mask.jpg', mask)
# cv2.imwrite('result.jpg', mask)