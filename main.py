import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import win32gui, win32ui, win32con
import uuid
from string import digits

""" def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

win32gui.EnumWindows( winEnumHandler, None ) """

# Load the model
model = load_model('models/v3/keras_model.h5')

# returns class number
def predict(image, title):   

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is 
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = image.convert('RGB')

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image.save('state/' + title + '.jpg')
    #turn the image(s) into a numpy array
    image_array = np.asarray(image)
    # Normalize the image(s)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    a_file = open("models/v3/labels.txt")
    first_prediction = np.argmax(prediction)

    # get 2nd best prediction (results in number that corresponds to class number in models/%version%/labels.txt)
    L = np.argsort(-prediction)
    second_prediction = L[:,1]
    # print(second_prediction)

    first_prediction_string = ''
    second_prediction_string = ''

    # enumerate over labels file to find the first prediction
    for position, line in enumerate(a_file):        
        if position == first_prediction:     
            table = str.maketrans('', '', digits)      
            string = line.translate(table)
            string = string.rstrip()
            string = string.strip()
            # Here I can save images into their champion folders to make training the model easier
            # image.save('automated/' + string + '/' + str(uuid.uuid4()) + '.png')
            first_prediction_string = string

        if position == second_prediction:
            table = str.maketrans('', '', digits)      
            string = line.translate(table)
            string = string.rstrip()
            string = string.strip()
            # Here I can save images into their champion folders to make training the model easier
            # image.save('automated/' + string + '/' + str(uuid.uuid4()) + '.png')
            second_prediction_string = string
    
    return first_prediction_string + ', ' + second_prediction_string
    

# Function to convert  
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 
    


# Window capture
def window_capture():    
    w = 1600 # set this
    h = 900 # set this    
    bmpfilenamename = "screenshot.bmp" #set this

    #hwnd = win32gui.FindWindow(None, 'Windows Media Player')
    hwnd = None

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

# capturing window
#window_capture()

# frame is now called out.bmp 
# split frame into smaller segments (FL1....FL14, BL1....BL14, B1....B9)
def process_board():
    board_array = []

    with Image.open("screenshot.bmp") as im:

        # The crop method from the Image module takes four coordinates as input.
        # The right can also be represented as (left+width)
        # and lower can be represented as (upper+height).
        FL_upper = 290
        FL_lower = 400

        #(left, upper, right, lower) = ()
        
        # Frontline first row
        FL1 = im.crop((415, FL_upper, 515, FL_lower))  
        FL2 = im.crop((515, FL_upper, 615, FL_lower))
        FL3 = im.crop((605, FL_upper, 705, FL_lower))   
        FL4 = im.crop((705, FL_upper, 805, FL_lower))   
        FL5 = im.crop((800, FL_upper, 900, FL_lower))
        FL6 = im.crop((895, FL_upper, 995, FL_lower))
        FL7 = im.crop((990, FL_upper, 1090, FL_lower))

        FL1_state = [predict(FL1, 'FL1'), predict(FL2, 'FL2'), predict(FL3, 'FL3'), predict(FL4, 'FL4'), predict(FL5, 'FL5'), predict(FL6, 'FL6'), predict(FL7, 'FL7')]
        #print("FL1:")
        #print([str(element) for element in FL1_state])

        # Frontline second row
        FL2_upper = FL_upper + 60
        FL2_lower = FL_lower + 70

        FL8 = im.crop((465, FL2_upper, 565, FL2_lower))
        FL9 = im.crop((565, FL2_upper, 665, FL2_lower))
        FL10 = im.crop((655, FL2_upper, 755, FL2_lower))
        FL11 = im.crop((755, FL2_upper, 855, FL2_lower))
        FL12 = im.crop((850, FL2_upper, 950, FL2_lower))
        FL13 = im.crop((945, FL2_upper, 1045, FL2_lower))
        FL14 = im.crop((1040, FL2_upper, 1140, FL2_lower))

        FL2_state = [predict(FL8, 'FL8'), predict(FL9, 'FL9'), predict(FL10, 'FL10'), predict(FL11, 'FL11'), predict(FL12, 'FL12'), predict(FL13, 'FL13'), predict(FL14, 'FL14')]
        #print("FL2:")
        #print([str(element) for element in FL2_state])

        # Backline first row
        BL_upper = 420
        BL_lower = 530

        BL1 = im.crop((400, BL_upper, 500, BL_lower))
        BL2 = im.crop((505, BL_upper, 605, BL_lower))
        BL3 = im.crop((600, BL_upper, 700, BL_lower))
        BL4 = im.crop((705, BL_upper, 805, BL_lower))  
        BL5 = im.crop((800, BL_upper, 900, BL_lower))
        BL6 = im.crop((905, BL_upper, 1005, BL_lower))
        BL7 = im.crop((1005, BL_upper, 1105, BL_lower))

        BL1_state = [predict(BL1, 'zBL1'), predict(BL2, 'zBL2'), predict(BL3, 'zBL3'), predict(BL4, 'zBL4'), predict(BL5, 'zBL5'), predict(BL6, 'zBL6'), predict(BL7, 'zBL7')]
        #print("BL1:")
        #print([str(element) for element in BL1_state])
        
        # Backline second row
        BL2_upper = 480
        BL2_lower = 590

        BL8 = im.crop((435, BL2_upper, 535, BL2_lower))
        BL9 = im.crop((540, BL2_upper, 640, BL2_lower))
        BL10 = im.crop((645, BL2_upper, 745, BL2_lower))
        BL11 = im.crop((755, BL2_upper, 855, BL2_lower))
        BL12 = im.crop((860, BL2_upper, 960, BL2_lower))
        BL13 = im.crop((965, BL2_upper, 1065, BL2_lower))
        BL14 = im.crop((1075, BL2_upper, 1175, BL2_lower))

        BL2_state = [predict(BL8, 'zBL8'), predict(BL9, 'zBL9'), predict(BL10, 'zBL10'), predict(BL11, 'zBL11'), predict(BL12, 'zBL12'), predict(BL13, 'zBL13'), predict(BL14, 'zBL14')]
        #print("BL2:")
        #print([str(element) for element in BL2_state])

        # Bench

        B_upper = 585
        B_lower = 695

        B1 = im.crop((300, B_upper, 400, B_lower))
        B2 = im.crop((400, B_upper, 500, B_lower))
        B3 = im.crop((510, B_upper, 610, B_lower))
        B4 = im.crop((610, B_upper, 710, B_lower))
        B5 = im.crop((705, B_upper, 805, B_lower))
        B6 = im.crop((800, B_upper, 900, B_lower))
        B7 = im.crop((895, B_upper, 995, B_lower))
        B8 = im.crop((990, B_upper, 1090, B_lower))
        B9 = im.crop((1090, B_upper, 1190, B_lower))

        B_state = [predict(B1, 'zzB1'), predict(B2, 'zzB2'), predict(B3, 'zzB3'), predict(B4, 'zzB4'), predict(B5, 'zzB5'), predict(B6, 'zzB6'), predict(B7, 'zzB7'), predict(B8, 'zzB8'), predict(B9, 'zzB9')]
        #print("Bench:")
        #print([str(element) for element in B_state])

        board_array = np.concatenate((FL1_state, FL2_state, BL1_state, BL2_state, B_state))

    first_predictions = []
    second_predictions = []

    for el in board_array:
        a, b = el.split(', ', 1)
        first_predictions.append(a)
        second_predictions.append(b)        

    return first_predictions, second_predictions

#first_predictions, second_predictions = process_board()
# Game state
# import time
# from python_imagesearch.imagesearch import imagesearch as search

# def onscreen(path, precision=0.8):
#     return search(path, precision)[0] != -1

# def main():
#     round21 = False        
#     # sleep until round 2-1
#     while not onscreen("./examples/2-1.png"):
#         time.sleep(1)
#     # only start from round 2.1 and further    
#     if onscreen("./examples/2-1.png") or round21:
#         print("I am inside the function now")
#         round21 = True
#         # first look for 'planning' image in game
#         if onscreen("./examples/planning.png"):
#             t_end = time.time() + 30
#             # now you are in the planning stage which takes 30 sec on normal rounds
#             while time.time() < t_end:
#                 # record screens for this amount of time
#                 window_capture() # Takes a screenshot through the Win32 API and saves the image as 'screenshot.bmp' in the root folder.
#                 process_board() # looks at FL1, FL2, BL1, BL2 and Bench. Returns board state incl. champion names in array format.
#                 # game_info() # Returns game information; health, round, level, money, streak, synergies, items (?)
                  # scout() # Does a quick overview of the other players info (synergies, health, eco etc.)
# while True:
#     main()
