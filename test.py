import glob
from cropper.cropper import *


save_dir = './res_non'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for image_dir in glob.glob('./images/*.jpg'):
    result = crop(image_dir)
    cv2.imwrite(os.path.join(save_dir, image_dir.split('/')[-1]), result)