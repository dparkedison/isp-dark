import cv2
import glob
import os

def islight(image, thresh=0.3):
    import numpy as np
    H, W = image.shape[:2]
    image = cv2.resize(image, (H//10, W//10))
    L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    L = L/np.max(L)
    mean = np.mean(L)
    return mean > thresh, mean * 100


os.makedirs("output/light", exist_ok=True)
os.makedirs("output/medium", exist_ok=True)
os.makedirs("output/dark", exist_ok=True)

for i, path in enumerate(glob.glob("images/*")):
    image = cv2.imread(path)
    if image is not None:
        path = os.path.basename(path)
        light, mean = islight(image)
        category = int(mean // 10)
        if category < 3:
            text = "dark"  
        elif category > 6:
            text = "light"  
        else:
            text = "medium"
        cv2.imwrite("output/{}/{}_{}".format(text, category, path), image)
        print(path, " L() =>", category, text)
    else:
        print(path)
