import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FFE7E7"
RED = "#944E63"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0

mytimer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps
    window.after_cancel(mytimer)
    canvas.itemconfig(title_text, text='Timer', fill=RED)
    canvas.itemconfig(timer_text, text='00:00')
    canvas.itemconfig(done_ticks, timer_text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 2 != 0:
        count_down(work_sec)
        canvas.itemconfig(title_text, text='Work', fill=RED)
    elif reps == 8:
        count_down(long_break_sec)
        canvas.itemconfig(title_text, text='Break', fill=GREEN)

        reps = 0
    elif reps % 2 == 0:
        count_down(short_break_sec)
        canvas.itemconfig(title_text, text='Break', fill=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global mytimer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    count_min = '{:02d}'.format(count_min)
    count_sec = '{:02d}'.format(count_sec)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        mytimer = window.after(1000, count_down, count - 1)
    elif count == 0:
        start_timer()
        work_done = math.floor(reps % 2)
        done_string = ""
        for i in range(work_done):
            done_string = done_string + "✔️"
        canvas.itemconfig(done_ticks, text=done_string)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro Timer")
# window.minsize()
window.config(padx=0, pady=0, bg=PINK)
window.grid()
canvas = Canvas(width=300, height=400, highlightthickness=0, bg=PINK)

# Load the .gif image file.
# gif1 = PhotoImage(file='cherry.gif')

frameCnt = 12
frames = [PhotoImage(file='cherry.gif', format='gif -index %i' % i) for i in range(frameCnt)]


def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    canvas.itemconfig(background, image=frame)
    window.after(150, update, ind)


# Put gif image on canvas.
# Pic's upper-left corner (NW) on the canvas is at x=50 y=10.


background = canvas.create_image(0, 0, anchor='nw')

timer_text = canvas.create_text(150, 250, text="00:00", fill=RED, font=(FONT_NAME, 35, "bold"))

button_s = Button(canvas, text="Start", bg='black', highlightbackground=PINK, command=start_timer)
canvas.create_window(100, 330, window=button_s)

button_r = Button(canvas, text="Reset", bg=RED, highlightbackground=PINK, command=reset)
canvas.create_window(200, 330, window=button_r)
title_text = canvas.create_text(150, 280, text="Timer", fill=RED, font=(FONT_NAME, 20, "normal"))
done_ticks = canvas.create_text(150, 380, fill=GREEN, font=(FONT_NAME, 10, "normal"))

canvas.grid(column=1, row=1)
window.after(0, update, 0)
window.mainloop()
