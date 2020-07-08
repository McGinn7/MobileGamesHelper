import aircv
import cv2


def resize(im, background_size, target_size, keep_aspect_ratio=True):
    im_size = im.shape[:2]
    scale_rate = []
    for i in range(2):
        scale_rate.append(float(target_size[i]) / background_size[i])
    scale_rate = min(scale_rate[0], scale_rate[1])
    for i in range(2):
        im_size[i] = int(scale_rate * im_size[i])
    im_resize = cv2.resize(im, im_size, interpolation=cv2.INTER_CUBIC)
    return im_resize


def detect_img_template(im_object, im_test, threshold, findall=False, rgb=True):
    if findall:
        return aircv.find_all_template(im_object, im_test, threshold, rgb)
    else:
        result = aircv.find_template(im_object, im_test, threshold, rgb)
        if result:
            # rect = result['rectangle']
            center_x = int(result['result'][0])
            center_y = int(result['result'][1])
            return center_x, center_y
        return []


# TODO: support object detection by sift
def detect_img_sift():
    pass
