from Textdetection import Text_detector
from Vocr import OCR
import cv2
import pickle
from preprocess_ocr import Preprocess_OCR
import re
import json
import numpy as np
from connector import Connector


class OCR_Document:
    def __init__(self,conn):
        self.text_detector=Text_detector()
        self.conn=conn
        self.index_key={} # id : {"first","end"} # first->end-1
        #self.setup_config()
        self.ocr=OCR()
        self.preprocess_ocr=Preprocess_OCR()
        self.img=None
        self.pattern_name=""
        

    #==================================================
   
    def setup_config(self,pattern_name):
        doc = self.conn.get_document(pattern_name)[0]

        self.attribute=doc['attribute']
        print(self.attribute)
        self.index_key={} 

    def get_indexs(self):
        print(self.list_texts)
        index_first=0
        index_last=len(self.list_texts)
        for att in self.attribute:
            if(att["type"]=="title"):
                
                for c in att['start_c'].split(";"):
                   index_cur=self.get_index_keyword(c,self.list_texts,index_first,-1)
                   if(index_cur!=-1):
                       index_first=index_cur
                       
                       break
                
         
                for c in att['end_c'].split(";"):
                    if(c=="-1"):
                       index_cur=len(self.list_texts)
                    else:
                        index_cur=self.get_index_keyword(c,self.list_texts,index_first,-1)
                    if(index_cur!=-1):
                       index_last=index_cur
                       break
                
                title=att['key_name']
                print()
                print("-"*20)
                
                print(title,"  ",index_first," ",index_last)

            else:
                index_f=-1
                index_l=-2
               
                for c in att['start_c'].split(";"):
                    print(c)
                    index_cur=self.get_index_keyword(c,self.list_texts,index_first,index_last)
                    
                    if(index_cur!=-1):
                        print(c,"   ",index_cur)
                        index_f=index_cur   
                        break
                
            
                for c in att['end_c'].split(";"):
                    index_cur=self.get_index_keyword(c,self.list_texts,index_first,index_last)
                    if(index_cur!=-1):
                        print(c,"   ",index_cur)
                        if(index_l==-2):
                            index_l=index_cur
                        else:
                            index_l=min(index_l,index_cur)
                       
                kn=att['key_name']
                print("---------------------------",kn,"--",index_f,"-------",index_l)
                if(index_f!=-1 and index_l!=-2):
                    for i in range(index_f,index_l):
                        print(self.list_texts[i])







    # function check
    def clean_str(self,s):
        s=s.strip()
        s=re.sub('[*&/`~@#$%\^&*]+', '', s)
        return s.lower()

    def compare_str(self,s1,s2):
        n1=len(s1)
        n2=len(s2)
        f=np.zeros((n1+1,n2+1))
        for i in range(n1+1):
            f[i][0]=1
        for j in range(n2+1):
            f[0][j]=1    
        f[0][0]=0
        if(s1[0]!=s2[0]):
            f[1][1]=1
        for i in range(0,n1):
            for j in range(0,n2):
                if(s1[i]==s2[j]):
                    f[i+1][j+1]=f[i][j]
                else:
                    f[i+1][j+1]=min(f[i][j],f[i+1][j],f[i][j+1])+1
        
        return f[n1][n2]

    def check_keyword(self,keyword,text,percent=0.3):
        keyword=self.clean_str(keyword)
        text=self.clean_str(text)
        n_keyword=len(keyword)
        n_text=len(text)
        similar=self.compare_str(keyword,text[:min(len(text),n_keyword)])
        similar_real=self.compare_str(keyword,text)
        return similar<=int(percent*min(n_keyword,n_text)),similar,similar_real
        

    def check_line(self,ct1,ct2,thresh_dis=25): #center 
        dis=abs(ct1[1]-ct2[1])
        return dis<thresh_dis
    #==========================================================

    #funtion get
    def get_center(self,dt_boxes,draw=True):
        image=self.img.copy()
        color = (0, 255, 0)
        #y,x
        list_centers=[]
        heights=[]
        for boxes in dt_boxes:
            heights.append(boxes[3][1]-boxes[0][1])
            heights.append(boxes[2][1]-boxes[1][1])
            x_center=int(sum(boxes[:,0])/4)
            y_center=int(sum(boxes[:,1])/4)
            list_centers.append((x_center,y_center))
            if(draw):
            
                image = cv2.line(image, (int(boxes[0][0]),int(boxes[0][1])), (int(boxes[1][0]),int(boxes[1][1])), color, 1) 
                image = cv2.line(image, (int(boxes[1][0]),int(boxes[1][1])), (int(boxes[2][0]),int(boxes[2][1])), color, 1) 
                image = cv2.line(image, (int(boxes[2][0]),int(boxes[2][1])), (int(boxes[3][0]),int(boxes[3][1])), color, 1)
                image = cv2.line(image, (int(boxes[3][0]),int(boxes[3][1])), (int(boxes[0][0]),int(boxes[0][1])), color, 1)
                image = cv2.circle(image,(x_center,y_center),1,color,1)
        if(draw):
            cv2.imwrite("output/image_with_boxes.jpg",image)
        self.height_mean=sum(heights)/len(heights)
        self.height_mean=int(self.height_mean/2)
        return list_centers

    def get_lines(self,first,last,list_centers): # output list of list index which perline
        lines=[[first]]
        for i in range(first+1,last):

            if(self.check_line(list_centers[i],list_centers[i-1],self.height_mean)):
                lines[-1].append(i)
            else:
                lines.append([i])
        return lines
    
    def get_index_keyword(self,keyword,list_text,begin,end):
        list_text=list_text.copy()
        if(end==-1):
            end=len(list_text)
        similar_min=1000
        similar_real_min=1000
        index_final=-1
        for i in range(begin,end):
            check,similar,similar_real=self.check_keyword(keyword,list_text[i])
            
            if check and similar < similar_min:
                similar_min=similar
                index_final=i
                similar_real_min=similar_real
            elif(similar==similar_min and similar_real<similar_real_min):
                similar_min=similar
                index_final=i
                similar_real_min=similar_real
        return index_final
    #========================================================

    #funtion sort
    def sort_x(self,x):
        return self.list_centers[x][0]
    
    def sort(self,center_ids):
        center_ids.sort(key=self.sort_x)
        return center_ids
    
    #==========================================================
    def prepare_ocr(self,image_origin,remove_red_word=True): # get list_center,list_text,list_box,list_line 
        # cv2.imshow("image_origin",img)
        self.img,det_imgs,dt_boxes=self.text_detector.detect(image_origin.copy())
        #cv2.imwrite("data/image.jpg",img)
        list_texts=[]
        if(remove_red_word):
            boxes_noises=self.preprocess_ocr.get_box_red_word(image_origin.copy())
            dt_boxes,det_imgs=self.preprocess_ocr.remove_boxes(boxes_noises, dt_boxes,det_imgs)
        for det_img in det_imgs:
            list_texts.append(self.ocr.predict(det_img))
        self.list_centers=self.get_center(dt_boxes)
        self.lines=self.get_lines(0,len(self.list_centers),self.list_centers) 
        ids=[]
        for x in self.lines:
            for y in self.sort(x):
                ids.append(y)
              
        self.list_texts=[]
        self.list_boxes=[]
        self.list_centers_new=[]
        for i in ids:
            self.list_texts.append(list_texts[i])
            self.list_boxes.append(dt_boxes[i])
            self.list_centers_new.append(self.list_centers[i])
        self.list_centers=self.list_centers_new
        self.n=len(self.list_texts)
    
    def search(self,keyword): # {"id":"id","parent_id":"","define":{"start_key":"first_key","end_key","last_key"}}
        first_index_par=0
        end_index_par=-1
        if(keyword["parent_id"]!=-1):
            first_index_par=self.index_key[keyword["parent_id"]]["first"]
            end_index_par=self.index_key[keyword["parent_id"]]["end"]
        first_index=self.get_index_keyword(keyword["define"]["start_key"],self.list_texts,first_index_par,end_index_par)
        if (first_index == -1 ):
            first_index=first_index_par
        end_index=self.get_index_keyword(keyword["define"]["end_key"],self.list_texts,first_index_par,end_index_par)
        self.index_key[keyword["id"]]={"first":first_index,"end":end_index}
    def get_text(self,id):
        for i in range(self.index_key[id]["first"],self.index_key[id]["end"]):
            print(self.list_texts[i]+" ")
                
    def main(self,image,pattern_name): # type #uyquyen,dkkd,bonhiem
        self.setup_config(pattern_name=pattern_name)
        self.prepare_ocr(image,remove_red_word=True)
        self.get_indexs()


if __name__=="__main__":
    conn=Connector("doc")
    ocr=OCR_Document(conn)
    
    # ocr.setup_config("giấy ủy nhiệm")
    
    img = cv2.imread("data/uyquyen.png")
  
    ocr.main(img,pattern_name="giấy ủy quyền")
    # keyword= {"id":0,"parent_id":-1,"define":{"start_key":"Bên ủy quyền","end_key":"bên được ủy quyền"}}
    # keyword1={"id":1,"parent_id":0,"define":{"start_key":"Ông","end_key":"Sinh ngày"}}
    # ocr.search(keyword)
    # print(ocr.index_key)
    # ocr.search(keyword1)
    # print(ocr.index_key)
    # ocr.get_text(0)
    # ocr.get_text(1)





        
        


