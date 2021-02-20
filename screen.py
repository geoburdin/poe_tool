import time
import pyautogui
from PIL import Image
import mss
from get_price import get_price
import clipboard
import cv2
import imutils
import numpy as np

pyautogui.FAILSAFE = False


def make_screenshot(rect):
    with mss.mss() as mss_instance:
        screenshot = mss_instance.grab(rect)

        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
        img.save('screenshot' + '.png', 'PNG')


stash = {"left": 17, "top": 150, "width": 580, "height": 580}
prices = []


def find_bright(img):
    pyautogui.moveTo(20, 20)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.click()
    image = cv2.imread(img)
    image_blur = cv2.medianBlur(image, 11)
    image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    image_res, image_thresh = cv2.threshold(image_blur_gray, 20, 255, cv2.THRESH_BINARY)
    cv2.imwrite('res.png', image_thresh)
    kernel = np.ones((7, 10), np.uint8)
    opening = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, kernel)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, last_image = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)
    last_image = np.uint8(last_image)
    cnts = cv2.findContours(last_image.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for (i, c) in enumerate(cnts):
        text = 'error in copypaste'
        ((x, y), _) = cv2.minEnclosingCircle(c)
        cv2.putText(image, "#{}".format(i + 1), (int(x) - 45, int(y) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        pyautogui.moveTo(int(x) + 17, int(y) + 150)

        pyautogui.hotkey('ctrl', 'c')
        text = clipboard.paste()
        print(text)
        if "price" not in text:
            price = get_price(str.join("\n", text.splitlines()), True)
            if 'Chaos' in price:
                price = price[:-6]
                print(price)
                cv2.imwrite('out.png', image)
                prices.append(price)

                pyautogui.rightClick(int(x) + 17, int(y) + 150, duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('select.png', confidence=0.5), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('exact.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('field_for_price.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.write(price, interval=0.25)
                ok = pyautogui.locateCenterOnScreen('ok.png', confidence=0.7)
                pyautogui.moveTo(ok, duration=0.1)
                pyautogui.click(duration=0.1)

            if 'Exalted' in price:
                price = price[:-8]
                print(price)
                cv2.imwrite('out.png', image)
                prices.append(price)

                pyautogui.rightClick(int(x) + 17, int(y) + 150, duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('select.png', confidence=0.5), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('exact.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('select_unit.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('exalted.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.moveTo(pyautogui.locateCenterOnScreen('field_for_price.png', confidence=0.7), duration=0.1)
                pyautogui.click(duration=0.1)

                pyautogui.write(price, interval=0.25)
                ok = pyautogui.locateCenterOnScreen('ok.png', confidence=0.7)
                pyautogui.moveTo(ok, duration=0.1)
                pyautogui.click(duration=0.1)

    return prices
