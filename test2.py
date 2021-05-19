import numpy as np
import cv2

image = cv2.imread('data/a.jpg')
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



cv2.imwrite('mask.jpg', mask)
cv2.imwrite('result.jpg', mask)