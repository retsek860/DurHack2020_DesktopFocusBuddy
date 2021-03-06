import pyautogui
import random
import tkinter as tk
import ctypes
import random
import os
import psutil
user32 = ctypes.windll.user32

y = user32.GetSystemMetrics(1) - 100 - 40
x = user32.GetSystemMetrics(0) - 100 - 300
cycle = 0
check = 1
idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
event_number = random.randrange(1,3,1)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def event(cycle,check,event_number,x):
    if event_number in idle_num:
        check = 0
        window.after(400,update,cycle,check,event_number,x) #no. 1,2,3,4 = idle
    elif event_number == 5:
        check = 1
        window.after(100,update,cycle,check,event_number,x) #no. 5 = idle to sleep
    elif event_number in walk_left:
        check = 4
        window.after(100,update,cycle,check,event_number,x)#no. 6,7 = walk towards left
    elif event_number in walk_right:
        check = 5
        window.after(100,update,cycle,check,event_number,x)#no 8,9 = walk towards right
    elif event_number in sleep_num:
        check  = 2
        window.after(1000,update,cycle,check,event_number,x)#no. 10,11,12,13,15 = sleep
    elif event_number == 14:
        check = 3
        window.after(100,update,cycle,check,event_number,x)#no. 15 = sleep to idle#making gif work 

def gif_work(cycle,frames,event_number,first_num,last_num):
    if cycle < len(frames) -1:
        cycle+=1
    else:
        cycle = 0
        event_number = random.randrange(first_num,last_num+1,1)
    return cycle,event_number

def update(cycle,check,event_number,x):
    global global_timer
    global window_timer
    global_timer += 1
    window_timer += 1
    #idle
    if check ==0:
        frame = idle[cycle]
        cycle ,event_number = gif_work(cycle,idle,event_number,1,9)
        create_textbox()
    #idle to sleep
    elif check ==1:
        frame = idle_to_sleep[cycle]
        cycle ,event_number = gif_work(cycle,idle_to_sleep,event_number,10,10)#sleep
    elif check == 2:
        frame = sleep[cycle]
        cycle ,event_number = gif_work(cycle,sleep,event_number,10,15)#sleep to idle
    elif check ==3:
        frame = sleep_to_idle[cycle]
        cycle ,event_number = gif_work(cycle,sleep_to_idle,event_number,1,1)#walk toward left
    elif check == 4:
        frame = walk_positive[cycle]
        cycle , event_number = gif_work(cycle,walk_positive,event_number,1,9)
        x -= 3#walk towards right
    elif check == 5:
        frame = walk_negative[cycle]
        cycle , event_number = gif_work(cycle,walk_negative,event_number,1,9)
        x -= -3
        
    window.geometry('100x100+'+str(x)+'+'+str(y))
    label.configure(image=frame)
    window.after(1,event,cycle,check,event_number,x)

def create_textbox():
    global window_open
    global window_timer
    if (window_open == False and window_timer > 50):
        window_open = True
        window2 = tk.Tk()

        my_text = getText()
        text_array = []
        cap = 20
        while len(my_text) > cap:
            i = cap - 2
            while my_text[i] != ' ' and i < len(my_text) and my_text[i] != '\n':
                i += 1
            text_array.append(my_text[:i])
            my_text = my_text[i+1:]
        text_array.append(my_text)
        my_text = '\n'.join(text_array)

        
        my_label = tk.Label(window2, text=my_text)
        my_label.config(font=("Courier", 20))
        my_label.pack(fill=tk.BOTH, expand=1)
        window2.title("Steppe")
        window2.geometry(str(cap*20 + 30)+'x'+str(len(text_array)*50)+'+'+str(int((user32.GetSystemMetrics(1) + cap*20 + 30)/2))+'+'+str(int(user32.GetSystemMetrics(1)/2)))
        
        def disable_event():
            global window_open
            global window_timer
            window_open = False
            window_timer = 0
            window2.destroy()
            
        window2.protocol("WM_DELETE_WINDOW", disable_event)
        window2.lift()

def getText():
    f = ''
    global global_timer
    if (global_timer > 1200):
        global_timer = 0
        f = open(resource_path("take_a_break.txt"), "r")
    else:
        if (isWorking()):
            n = random.randint(1,3)
            if n == 1:
                f = open(resource_path("jokes.txt"), "r")
            if n == 2:
                f = open(resource_path("interesting_facts.txt"), "r")
            if n == 3:
                f = open(resource_path("positive_feedback.txt"), "r")
        else:
            f = open(resource_path("lazy.txt"), "r")
    return random_line(f)
    

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num): continue
        line = aline
    return line

def isWorking():
    for p in psutil.process_iter():
        if (p.name() == "steam.exe" or p.name() == "UplayWebCore.exe" or p.name() == "Origin.exe" or p.name() == "Battle.net.exe" or p.name() == "EpicGamesLauncher.exe"):
            return False

    return True


window = tk.Tk()#call buddy's action gif

idle = [tk.PhotoImage(file=resource_path('idle.gif'),format = 'gif -index %i' %(i)) for i in range(2)]#idle gif
idle_to_sleep = [tk.PhotoImage(file=resource_path('idle_to_sleep.gif'),format = 'gif -index %i' %(i)) for i in range(3)]#idle to sleep gif
sleep = [tk.PhotoImage(file=resource_path('sleep.gif'),format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif
sleep_to_idle = [tk.PhotoImage(file=resource_path('sleep_to_idle.gif'),format = 'gif -index %i' %(i)) for i in range(6)]#sleep to idle gif
walk_positive = [tk.PhotoImage(file=resource_path('jumping2.gif'),format = 'gif -index %i' %(i)) for i in range(9)]#walk to left gif
walk_negative = [tk.PhotoImage(file=resource_path('jumping.gif'),format = 'gif -index %i' %(i)) for i in range(9)]#walk to right gif


#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')

window_open = False
window_timer = 0
global_timer = 0

label.pack()#loop the program
window.after(1,update,cycle,check,event_number,x)
window.lift()
window.mainloop()
