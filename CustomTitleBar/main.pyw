from tkinter import *
# import customtkinter as ct
from PIL import Image, ImageTk
from ctypes import windll
import cProfile

tk_title = "\tApplication" 

root = Tk()
root.title(tk_title) 
root.iconbitmap("images\\icon.ico")
root.overrideredirect(True)

win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()
root.geometry(f'{win_width-350}x{win_height-200}+75+75')
root.minimized = False 
root.maximized = False 

LGRAY = '#3e4042'
DGRAY = '#25292e' 
RGRAY = '#10121f' 
# RGRAY = '#222' 

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)

def set_appwindow(mainWindow): 
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

def deminimize(event):
    # root.focus() 
    root.attributes("-alpha", 2)
    if root.minimized == True:
        root.minimized = False        

def minimize_me():
    root.after(10, lambda: fade_out(root))

def maximize_me():
    if root.maximized == False:
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ", image=my_minimise_icon)
        root.after(10, lambda: fade_out(root))
        root.after(200, lambda: root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-40}+0+0"))
        root.after(300, lambda: fade_in(root))
        root.maximized = not root.maximized 
    else:
        expand_button.config(text=" 🗖 ", image=my_max_icon)
        root.after(10, lambda: fade_out(root))
        root.after(200, lambda: root.geometry(root.normal_size))
        root.after(300, lambda: fade_in(root))
        root.maximized = not root.maximized

def fade_out(widget):
    alpha = widget.attributes("-alpha")
    if alpha > 0:
        alpha -= 0.1
        widget.attributes("-alpha", alpha)
        widget.after(10, lambda: fade_out(widget))

def fade_in(widget):
    alpha = widget.attributes("-alpha")
    if alpha < 1:
        alpha += 0.1
        widget.attributes("-alpha", alpha)
        widget.after(10, lambda: fade_in(widget))

def fade_out_close(widget):
    alpha = widget.attributes("-alpha")
    if alpha > 0:
        alpha -= 0.4
        widget.attributes("-alpha", alpha)
        widget.after(10, lambda: fade_out(widget))
    
    root.destroy()

my_project_icon_src = Image.open("images\\icon.png")
my_project_icon = ImageTk.PhotoImage(my_project_icon_src.resize((35, 35)))

my_close_icon_src = Image.open("images\\x.png")
my_close_icon = ImageTk.PhotoImage(my_close_icon_src.resize((20, 20)))

my_max_icon_src = Image.open("images\\max.png")
my_max_icon = ImageTk.PhotoImage(my_max_icon_src.resize((20, 20)))

my_min_icon_src = Image.open("images\\minus.png")
my_min_icon = ImageTk.PhotoImage(my_min_icon_src.resize((20, 20)))

my_minimise_icon_src = Image.open("images\\min.png")
my_minimise_icon = ImageTk.PhotoImage(my_minimise_icon_src.resize((20, 20)))

Label(title_bar, bg=RGRAY, image=my_project_icon).pack(side=LEFT, padx=5)

close_button = Button(title_bar, text=' × ', command=lambda: fade_out_close(root),bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',
                    highlightthickness=0, image=my_close_icon, activebackground=RGRAY)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=0,bd=0,fg='white',font=("calibri", 13),
                    highlightthickness=0, image=my_max_icon, activebackground=RGRAY)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),
                    highlightthickness=0, image=my_min_icon, activebackground=RGRAY)
title_bar_title = ct.CTkLabel(title_bar, text=tk_title, font=("consolas", 20), text_color="white")

window = Frame(root, bg=DGRAY,highlightthickness=0)

title_bar.pack(fill=X)
close_button.pack(side=RIGHT,   ipadx=14, ipady=10)
expand_button.pack(side=RIGHT,  ipadx=14, ipady=10)
minimize_button.pack(side=RIGHT,ipadx=14, ipady=10)
title_bar_title.pack(side=TOP, pady=10, anchor="center")

window.pack(expand=True, fill=BOTH)

def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'    
    
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY
    
def change_size_on_hovering(event):
    global expand_button
    expand_button['bg']=LGRAY
    
def return_size_on_hovering(event):
    global expand_button
    expand_button['bg']=RGRAY
    
def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
    
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY
    
def get_pos(event):
    if root.maximized == False:
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root
        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

        def release_window(event):
            root.config(cursor="arrow")
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos)
title_bar_title.bind('<Button-1>', get_pos) 
close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

root.bind("<FocusIn>", deminimize)
root.after(10, lambda: set_appwindow(root))
root.bind("<Control-q>", lambda event: root.destroy())


cProfile.run("root.mainloop()")
