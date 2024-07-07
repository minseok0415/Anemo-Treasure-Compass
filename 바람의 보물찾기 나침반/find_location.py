import cv2
import numpy as np
from PIL import ImageGrab

CAPTURE_WIDTH = 60
CAPTURE_HEIGHT = 100
CAPTURE_X = 90
CAPTURE_Y = 75
CAPTURE_WEIGHT = 90
FULL_IMAGE_PATH = "images/map.png"
SAVE_IMAGE_PATH = "images/found_location.png"

def find_template_in_image(full_image_gray, template_image_gray):
    result = cv2.matchTemplate(full_image_gray, template_image_gray, cv2.TM_CCOEFF_NORMED)
    return np.where(result == np.max(result)), np.max(result)

def capture_image(x, y, width, height):
    capture = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    capture_np = np.array(capture)
    capture_bgr = cv2.cvtColor(capture_np, cv2.COLOR_RGBA2BGR)
    return capture_bgr

def loc():
    full_image = cv2.imread(FULL_IMAGE_PATH)
    full_image_gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
    
    capture_left = capture_image(CAPTURE_X, CAPTURE_Y, CAPTURE_WIDTH, CAPTURE_HEIGHT)
    positions_left, accuracy_left = find_template_in_image(full_image_gray, cv2.cvtColor(capture_left, cv2.COLOR_BGR2GRAY))
    
    capture_right = capture_image(CAPTURE_X + CAPTURE_WEIGHT, CAPTURE_Y, CAPTURE_WIDTH, CAPTURE_HEIGHT)
    positions_right, accuracy_right = find_template_in_image(full_image_gray, cv2.cvtColor(capture_right, cv2.COLOR_BGR2GRAY))
    
    for_return = ()
    
    if accuracy_left >= accuracy_right:
        match_image = full_image[positions_left[0][0]:positions_left[0][0]+CAPTURE_HEIGHT, positions_left[1][0]:positions_left[1][0]+CAPTURE_WIDTH]
        merged_image = np.hstack((capture_left, match_image))
        cv2.imwrite(SAVE_IMAGE_PATH, merged_image)
        for_return = (positions_left[0][0], positions_left[1][0], accuracy_left)
        
    else:
        match_image = full_image[positions_right[0][0]:positions_right[0][0]+CAPTURE_HEIGHT, positions_right[1][0]:positions_right[1][0]+CAPTURE_WIDTH]
        merged_image = np.hstack((capture_right, match_image))
        cv2.imwrite(SAVE_IMAGE_PATH, merged_image)
        for_return = (positions_right[0][0], positions_right[1][0] - 90, accuracy_right)
        
    if 169 <= for_return[1] <= 982 and 974 <= for_return[0] <= 1499:
        new_y = for_return[0] // 3 + 15
        new_x = for_return[1] // 3 + 813 // 3 * 2 + 5
        return (new_y, new_x, for_return[2])
        
    return for_return

if __name__ == "__main__":
    print(loc())