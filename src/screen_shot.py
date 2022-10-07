from PIL import ImageGrab
import keyboard

idx = 0
def screen_shot():
    global idx
    file = str(idx)
    rect = (0, 0, 1920, 1080)
    print(file, rect)
    screenshot = ImageGrab.grab()
    croped_screenshot = screenshot.crop(rect)
    croped_screenshot.save(file + '.jpg')
    idx += 1

keyboard.add_hotkey('right',screen_shot)
keyboard.wait()