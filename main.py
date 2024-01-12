import os
import pyautogui as pg
import random
from time import sleep
import json
# type like a human

fileinput = "text.txt"# if you want to read from a file

typing_slow = 10# the max typing delay (ms)
typing_fast = 2# the min typing delay (ms)
speed_change = 99#95# the chance of changing the typing speed each letter


error_waitchance = 80# chance that the ai will pause after making an error
error_waittime = 0.5# max amount of seconds the ai will wait after making an error
error_chance = 2# chance to make an error every iteration
error_size = 5# max size of errors the ai can make
error_in_error = 5# chance that an error will be made in the error
max_error_recusions = 2# maximum errors inside errors, never set to 0 because that will disable errors alltogether


if not os.path.exists(fileinput) and fileinput != "":
    print("Provided file does not exist!")
    exit()

if fileinput != "":
    with open(fileinput, "r") as e:
        content = e.read()

    if content == "" or content is None or content == "\n":
        print("There is nothing in the file!")
        exit()

else:
    content = input("Enter text to type here: ")

with open("keymap.json", "r") as e:
    try:
        keymap = json.load(e)   # TODO put the keys and each key close to it
    except Exception as e:
        keymap = {}
        print(f"Failed to read keymap: {str(e)}")
        #for i in chars:
        #    keymap[i] = [random.choice(chars)]
    else:
        print("Loaded keymap")

input("press enter to start typing: ")
print("typing will start in 5 seconds\n")

for i in range(5):
    print(5-(i))
    sleep(1)

# contstants
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890?.!"

pg.PAUSE = 0



def do_error(cur, error_sizez, recur=0):

    if (cur + error_sizez) > len(content)-1:
        diff = (cur + error_sizez) - len(content-1)
        if error_sizez - diff <= 0:
            return
        else:
            error_sizez -= diff

    fix_seq = ""
    error_amount = error_sizez
    error_passed = 0
    undo_error = False
    first_undo_iter = False

    if recur > max_error_recusions:
        return
    
    for i in range(error_sizez*2):
        if random.randint(1,100) <= speed_change:
            pg.PAUSE = (random.randint(typing_fast,typing_slow)/100)

        if random.randint(1,100) <= error_in_error:
            do_error(cur+error_sizez,random.randint(0, error_size), recur+1)
        
        if not undo_error and (error_passed != error_amount):# create the error

            actual_index = cur+error_passed
            

            #print(actual_index)
            #print(content[actual_index])
            #print((content[actual_index].lower() in keymap))
            #print(keymap[content[actual_index].lower()])
            
            if content[actual_index].lower() in keymap:
                selected = random.choice(keymap[content[actual_index].lower()])
            else:
                selected = random.choice(chars)
            
            if content[cur+error_passed].islower():
                pg.press(selected.lower())
            else:
                pg.press(selected.upper())

            error_passed += 1
            fix_seq += content[index]
        
        elif error_passed == error_amount:
            undo_error = True

        if undo_error:
            if random.randint(0,100) < error_waitchance and not first_undo_iter and recur == 0:
                sleep(
                    random.randint(0,error_waittime*10)/10
                    )
            elif random.randint(0,100) < error_waitchance and not first_undo_iter and recur > 0:
                sleep(
                    (random.randint(0,error_waittime*10)/10)/2
                    )

            if error_passed == 0:
                return
            pg.press("backspace")
            error_passed -= 1
            first_undo_iter = True 

for index in range(len(content)):
    if random.randint(1,100) <= speed_change:
        pg.PAUSE = (random.randint(typing_fast,typing_slow)/100)

    if random.randint(1,100) <= error_chance:
        do_error(index, random.randint(1,error_size))
         

    
    pg.press(content[index])
