from libpyk4a import Config, PyK4A
import libpyk4a as pyk4a
import numpy as np
import cv2


def cam_initialize():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=False,
        )
    )
    k4a.start()
    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510
    
    return k4a

def ir_preprocess(fr):
    img = np.stack((fr,)*3, axis=-1)
    return (img/256).astype(np.uint8)

def modify_contrast_and_brightness(img,a=2.0,b=0.0):
    out = img.copy()
    array_alpha = np.array([a]) # contrast 
    array_beta = np.array([b]) # brightness

    out = cv2.add(out, array_beta)                    

    # multiply every pixel value by alpha
    out = cv2.multiply(out, array_alpha)

    # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
    out = np.clip(out, 0, 65535)
    return out