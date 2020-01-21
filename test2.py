import tkinter


def show():
    win = tkinter.Tk()
    win.title('猜燈謎')
    win.geometry('600x500')

    img = tkinter.PhotoImage(file='./giphy.gif')
    label_img = tkinter.Label(win, image = img)
    label_img.pack()
    win.mainloop()

# show()
