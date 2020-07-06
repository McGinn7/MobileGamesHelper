import aircv


def detect_img_template(im_object, im_test, threshold, findall=False, rgb=True):
    if findall:
        return aircv.find_all_template(im_object, im_test, threshold, rgb)
    else:
        return aircv.find_template(im_object, im_test, threshold, rgb)


# TODO: support object detection by sift
def detect_img_sift():
    pass
