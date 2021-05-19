import matplotlib.pyplot as plt
from PIL import Image

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2


class OCR:
    def __init__(self,config_name="vgg_transformer"):
        config = Cfg.load_config_from_name(config_name)
        # config['weights'] = 'https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA'
        config['cnn']['pretrained']=True
        config['device'] = 'cuda:0'
        config['predictor']['beamsearch']=False
        self.detector = Predictor(config)
        
    def predict(self,img):#cv2
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        s = self.detector.predict(img)
        return s


if __name__ == "__main__":
    x=OCR()
    img=cv2.imread("a.png")
    s=x.predict(img)
    print(s)
