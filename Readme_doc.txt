#bai toán :
    trích xuất thông tin từ ảnh tài liệu

    # về client:
        Nếu template đã được lưu trước đó thì có thể chọn ngược lại tự thêm template
    
    # về cấu trúc template :
        define các trường như mục lục
        #example
          {"bonhiem:
            {"_Header":["QUYẾT ĐỊNH CỦA GIÁM ĐỐC","Căn cứ vào Điều lệ","Căn cứ vào Biên bản họp","Căn cứ vào yêu cầu","Xét năng lực"]})
            {"QUYẾT ĐỊNH":[]})
            {"Điều 1:Nay bổ nhiệm":["Họ và tên","Giới tính","Sinh ngày","Dân tộc","Quốc tịch","CMTNN/Hộ chiếu số","Nơi đăng ký HKTT","Chỗ ở hiện tại","Giữ chức vụ"]})
            {"Điều 2":["_content"]})
            {"Điều 3":["_content"]})
            {"_End":["Nơi nhận"]})
          }
          {"dkkd":
            {"_Header":["Mã Số Doanh Nghiệp","Đăng ký lần đầu","Đăng ký thay đổi lần thứ"]}
            {"1.Tên công ty":["Tên Công ty viết bằng tiếng Việt","Tên công ty viết bằng tiếng nước ngoài","Tên công ty viết tắt"]}
            {"2.Địa chỉ trụ sở chính":["_Địa chỉ","Điện thoại","Fax","Email","Website"]}
            {"3.Vốn điều lệ":["Vốn điều lệ","Bằng Chữ","Mệnh giá cổ phần","Tổng số cổ phần"]}
            {"4.Người đại diện theo pháp luật của công ty":["Họ và tên","Giới tính","Chức danh","Sinh ngày","Dân tộc","Quốc tịch","Loại giấy tờ chứng thực cá nhân","Ngày cấp","Nơi cấp","Nơi đăng kí hộ khẩu thường trú","Chỗ ở hiện tại"]}
            {"_End":["TRƯỞNG PHÒNG"]}
           
           }

#solution:
    # các thuật toán AI
        detect line : https://github.com/PaddlePaddle/PaddleOCR
            input : image
            output : list of [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        ocr :
            Vietocr: https://github.com/pbcquoc/vietocr
            input : 
                image of crop output detect line
            output :
                text
    # thuat toan xử lý thuần :
        -loai bo cac dong chữ màu đỏ : preprocess_ocr.py
            -detect red region : 
            -loai bo red lines : 
                - trích xuất vùng màu đỏ : red_word.jpg
                - detect line trong ảnh 
                - dung iou de loai cac chu mau do

        - săp xếp lại các line chữ : funtion get_lines in main.py
            - Sắp xếp theo trục y:(output detectline)
            - Tinh height các box line => tính height trung bình (funtion get_center)=> khoảng cách ngắn nhất 2 line box_mean//2 
            - group các box cùng line
            - sắp xếp theo x
            
        - Kiểm tra độ lệch 2 xâu (funtinon compare_str in main.py)
            Input 2 xâu
            Output số bước ít nhất thêm sửa xóa để 2 xâu giống nhau  (thuật toán qui hoạch động)
        - Lấy xâu khớp trong list xâu :
            Duyệt list xâu và tính độ lệch 2 xâu :
                index thỏa mãn :
                    độ lệch <= percent*min(len(keyword),len(str))

        - Xây dựng luật dựa trên template (main.py)

                

    #Quy trình
        B1 : Loại bỏ nhiễu : (preprocess_ocr.py)
        B2: Xây dựng lại thứ tự các box phù hợp (boxA trên boxB không có nghĩa yA<yB) (main.py)
        B2 : Lấy text (Vocr.py)
        B3 : Xây dựng rule (main.py)
        B4 : Xuất output (main.py)


#Testapi:
    192.168.100.62:1313/docs#/
    input:
        type : dkkd,bonhiem,uyquyen
        single_image 
    output :
        json theo template đặt ra

    #example image :
        data/dkkd.png
        data/bonhiem.png
        data/uyquyen.png
# Định hướng tiếp theo:
    - Xây dựng ứng dụng đầy đủ để cho phép người dung tự đặt template
    - Xây dựng mức tổng quát hơn nữa
    - Xử lý dạng bảng
    - Check dòng phù hợp hơn bằng các template như gạch đầu dòng ...



