import tools.infer.predict_det as predict_det
import tools.infer.utility as utility
import copy
import cv2
import numpy as np
class Text_detector:
    def __init__(self):
        args = utility.parse_args()
        args.det_model_dir="./inference/ch_ppocr_server_v2.0_det_infer/"
        self.text_detector = predict_det.TextDetector(args)
        self.color = (255,255,255)
        self.boder_size=100

    def sorted_boxes(self,dt_boxes):
        """
        Sort text boxes in order from top to bottom, left to right
        args:
            dt_boxes(array):detected text boxes with shape [4, 2]
        return:
            sorted boxes(array) with shape [4, 2]
        """
        num_boxes = dt_boxes.shape[0]
        sorted_boxes = sorted(dt_boxes, key=lambda x: (x[0][1], x[0][0]))
        _boxes = list(sorted_boxes)

        for i in range(num_boxes - 1):
            if abs(_boxes[i + 1][0][1] - _boxes[i][0][1]) < 10 and \
                    (_boxes[i + 1][0][0] < _boxes[i][0][0]):
                tmp = _boxes[i]
                _boxes[i] = _boxes[i + 1]
                _boxes[i + 1] = tmp
        return _boxes

    def get_rotate_crop_image( self,img, points):
        '''
        img_height, img_width = img.shape[0:2]
        left = int(np.min(points[:, 0]))
        right = int(np.max(points[:, 0]))
        top = int(np.min(points[:, 1]))
        bottom = int(np.max(points[:, 1]))
        img_crop = img[top:bottom, left:right, :].copy()
        points[:, 0] = points[:, 0] - left
        points[:, 1] = points[:, 1] - top
        '''
        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))+15
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))+15
            
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                              [img_crop_width, img_crop_height],
                              [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points, pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img

    def detect(self,img):

        img=cv2.copyMakeBorder(img, self.boder_size, self.boder_size, self.boder_size, self.boder_size, cv2.BORDER_CONSTANT,
            value=self.color)
        dt_boxes, elapse = self.text_detector(img)
        dt_boxes = self.sorted_boxes(dt_boxes)
        # print("dt_boxes",dt_boxes)
        img_crop_list=[]
        for bno in range(len(dt_boxes)):
            tmp_box = copy.deepcopy(dt_boxes[bno])
            img_crop = self.get_rotate_crop_image(img, tmp_box)
            img_crop=cv2.copyMakeBorder(img_crop, 2 ,2, 10, 10, cv2.BORDER_CONSTANT,value=self.color)
            img_crop_list.append(img_crop)

        return img,img_crop_list,dt_boxes