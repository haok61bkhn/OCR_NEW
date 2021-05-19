from Textdetection import Text_detector
from Vocr import OCR
import cv2
import pickle
from preprocess_ocr import Preprocess_OCR
import re
import json
import numpy as np


class OCR_Document:

    def __init__(self):
        self.text_detector=Text_detector()
        #self.setup_config()
        self.ocr=OCR()
        self.preprocess_ocr=Preprocess_OCR()
        self.img=None

    #==================================================
    #funtion setup
    def setup_config(self,type):
        self.Contents={}
      
        #=========bonhiem==========
        if(type=="bonhiem"):
            self.Contents.update({"_Header":["QUYẾT ĐỊNH CỦA GIÁM ĐỐC","Căn cứ vào Điều lệ","Căn cứ vào Biên bản họp","Căn cứ vào yêu cầu","Xét năng lực"]})
            self.Contents.update({"QUYẾT ĐỊNH":[]})
            self.Contents.update({"Điều 1:Nay bổ nhiệm":["Họ và tên","Giới tính","Sinh ngày","Dân tộc","Quốc tịch","CMTNN/Hộ chiếu số","Nơi đăng ký HKTT","Chỗ ở hiện tại","Giữ chức vụ"]})
            self.Contents.update({"Điều 2":["_content"]})
            self.Contents.update({"Điều 3":["_content"]})
            self.Contents.update({"_End":["Nơi nhận"]})

        #=========dkkd=============
        elif(type=="dkkd"):
            self.Contents.update({"_Header":["Mã Số Doanh Nghiệp","Đăng ký lần đầu","Đăng ký thay đổi lần thứ"]})
            self.Contents.update({"1.Tên công ty":["Tên Công ty viết bằng tiếng Việt","Tên công ty viết bằng tiếng nước ngoài","Tên công ty viết tắt"]})
            self.Contents.update({"2.Địa chỉ trụ sở chính":["_Địa chỉ","Điện thoại","Fax","Email","Website"]})
            self.Contents.update({"3.Vốn điều lệ":["Vốn điều lệ","Bằng Chữ","Mệnh giá cổ phần","Tổng số cổ phần"]})
            self.Contents.update({"4.Người đại diện theo pháp luật của công ty":["Họ và tên","Giới tính","Chức danh","Sinh ngày","Dân tộc","Quốc tịch","Loại giấy tờ chứng thực cá nhân","Ngày cấp","Nơi cấp","Nơi đăng kí hộ khẩu thường trú","Chỗ ở hiện tại"]})
            self.Contents.update({"_End":["TRƯỞNG PHÒNG"]})
        #=========uyquyen=========
        elif(type=="uyquyen"):
            
            self.Contents.update({"_Header":["Giấy ủy quyền này"]})
            self.Contents.update({"BÊN ỦY QUYỀN":["Ông","Sinh ngày","Dân tộc","Quốc tịch","Chứng minh thư nhân dân số","Nơi đăng ký hổ khẩu thường trú","Chức vụ"]})
            self.Contents.update({"BÊN ĐƯỢC ỦY QUYỀN:":["Ông","Sinh ngày","Dân tộc","Quốc tịch","Chứng minh thư nhân dân số","Nơi đăng ký hổ khẩu thường trú","Chức vụ","1. NỘI DUNG VÀ PHẠM VI ỦY QUYỀN","2. TRÁCH NHIỆM CÁC BÊN","3. THỜI HẠN ỦY QUYỀN"]})
            self.Contents.update({"_End":["BÊN ĐƯỢC ỦY QUYỀN"]})
        
            
        #==========Thư báo giá===========
        elif(type=="thubaogia"):
            self.Contents.update({"_Header":["Ngày báo giá","1 Khách hàng","2 Địa chỉ","3 Tên người mua","Điện thoại","4 Email","Hiệu lực báo giá","Mã số báo giá"]})
            self.Contents.update({"Chúng tôi gửi tới Quý khách hàng":["_content"]})
            self.Contents.update({"Ghi chú":["_content"]})
            self.Contents.update({"_End":["Xác nhận đặt hàng"]})

        #=============Hồ sơ pháp ly==============
        # self.Contents.update({"_Header":["Mã doanh nghiệp","Đăng ký lần đầu","Đăng ký thay đổi lần thứ"]})
        # self.Contents.update({"1.Tên công ty":["Tên công ty viết bằng tiếng Việt","Tên công ty viết bằng tiếng nước ngoài","Tên công ty viết tắt"]})
        # self.Contents.update({"2.Địa chỉ trụ sở chính":["_address","Điện thoại","Fax","Email","Website"]})
        # self.Contents.update({"3.Vốn điều lệ":["Bằng chữ"]})
        # self.Contents.update({"4.Thông tin về chủ sở hữu":["Họ và tên","Giới tính","Sinh ngày","Dân tộc","Quốc tịch","Loại giấy tờ chứng thực cá nhân","Số giấy chứng thực cá nhân","Ngày cấp","Nơi cấp","Nơi đăng ký hộ khẩu thường trú","Chỗ ở hiện tại"]})
        # self.Contents.update({"5.Người đại diện theo pháp luật của công ty":["Họ và tên","Giới tính","Chức danh","Sinh ngày","Dân tộc","Quốc tịch","Loại giấy tờ chứng thực cá nhân","Số giấy chứng thực cá nhân","Ngày cấp","Nơi cấp","Nơi đăng ký hộ khẩu thường trú","Chỗ ở hiện tại"})
        # self.Contents.update({"_End":["TRƯỞNG PHÒNG"]})




        self.Keywords0=list(self.Contents.keys())
        for x in self.Keywords0:
            self.Contents[x].append("_end")
        print("________________________content__________________________" )
        print(self.Contents)
        self.indexs={"_Header":0}

    def set_up_indexs(self): #set indexs keywords0 
        for keyword in self.Keywords0[1:-1]:
            index=self.get_index_keyword(keyword,self.list_texts,0,len(self.list_texts))
            if(index == -1 ):
                print(keyword,"  ",-1)
            else:
                print(keyword,"   :  ",index,self.list_texts[index])
            self.indexs[keyword]=index
            
        if(self.Contents["_End"][0]!="None" and self.indexs[self.Keywords0[-2]]!=-1 ):
            index=self.get_index_keyword(self.Contents["_End"][0],self.list_texts,self.indexs[self.Keywords0[-2]]+1,len(self.list_texts))
            self.indexs["_End"]=index
        else:
            self.indexs["_End"]=self.n
    
    def set_up_indexs_child(self): # setup indexs child
        self.indexs_child={}
        for id,keyword0 in enumerate(self.Keywords0[:-1]):
            print("-------------------------",keyword0,"--------------------------------")
            begin=self.indexs[keyword0]+1
            if(begin!=-1):
                end=self.indexs[self.Keywords0[id+1]]
                indexs1={}
                keywords1=self.Contents[keyword0]
                for keyword in keywords1[:-1]:
                    if(keyword[0]!="_"):
                        index=self.get_index_keyword(keyword,self.list_texts,begin,end)
                        if(index!=-1):
                            begin = index
            #                 print(keyword,"   ",list_texts_new[index])
                        indexs1[keyword]=index
                    else:
                        indexs1[keyword]=begin
                self.indexs_child[keyword0]=indexs1
            else:
                self.indexs_child[keyword0]={}
        last=self.indexs["_End"]
        for i in range(len(self.Keywords0)-2,-1,-1):
            self.indexs_child[self.Keywords0[i]]["_end"]=last
            if(self.indexs[self.Keywords0[i]]!=-1):
                last=self.indexs[self.Keywords0[i]]
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
    
    def show_output(self):
        output_json={}
        for title in list(self.indexs_child.keys()):
            print("________________"+title+"________________")
            print()
            output_json[title]={}
            if(self.indexs[title]!=-1):
                index_title=self.indexs_child[title]
                keywords_title=list(index_title)
            
                for i in range(len(keywords_title)-1):
                    kw=keywords_title[i]
                    output_json[title][kw]=""
                    if(index_title[kw]!=-1):
                        begin= index_title[kw]
                        end=index_title[keywords_title[i+1]]
                        # for k in range(self.indexs[title],begin):
                        #     print(self.list_texts[k],end=" ")
                        print()
                        print("=============",kw,"==============")
                        
                        for k in range(begin,end):
                            print(self.list_texts[k],end=" ")
                            output_json[title][kw]+=self.list_texts[k]+" "
                        print()
            print()
            print()
        json.dump(output_json,open("output.json","w+"),ensure_ascii=False)
        return output_json
                
    def main(self,image,type): # type #uyquyen,dkkd,bonhiem
        self.setup_config(type=type)
        self.prepare_ocr(image,remove_red_word=True)
        self.set_up_indexs()
        print("_________indexs___________")
        print(self.indexs)
        print("_________end_indexs________")
        self.set_up_indexs_child()
        print("__________indexs_child_________")
        print(self.indexs_child)
        print("________end_indexs_child_______")
        return self.show_output()


if __name__=="__main__":
    ocr=OCR_Document()
    img = cv2.imread("data/uyquyen.png")
  
    ocr.main(img,type="uyquyen")




        
        


