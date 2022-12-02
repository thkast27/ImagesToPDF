import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
from PIL import Image
import uuid

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

BG_COLOR = '#2B3A55'
LABEL_BG = '#2B3A55'
LTEXT_COLOR = '#E8C4C4'
MAIN_LABEL_FONT = ('Helvetica', 14, 'italic')
OUT_LABEL_FONT = ('Helvetica', 10, 'italic')
BTNS_FONT = ('Helvetica', 8)
BTNS_BG = '#E8C4C4'


def submit():
    global itemlist
    itemlist = lb.get(0, tk.END)
    image_list = []
    out_path = output_path.get() + ".pdf"
    for img in itemlist:
        img = Image.open(fr'{img}')
        img = img.convert('RGB')
        image_list.append(img)
    try:
        file_exists = os.path.exists(out_path)
        if file_exists:
            ending = out_path[:-4]
            id = uuid.uuid4()
            out_path = ending +str(id) + ".pdf"
        image_list[0].save(fr'{out_path}', save_all=True, append_images=image_list[1:])
    except IndexError:
        print("Please add some images first")
    finally:
        print("Your convert was successful")


def clear():
    lb.delete(0, tk.END)


def delete():
    lb.delete(tk.ANCHOR)


root = TkinterDnD.Tk()
root.geometry("600x300")
root.resizable(False, False)
root.title('Images To PDF')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root['background'] = BG_COLOR

style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', font=BTNS_FONT, background=BTNS_BG)
style.configure('TLabel', background=LABEL_BG, font=MAIN_LABEL_FONT, foreground=LTEXT_COLOR)

label = ttk.Label(text="Drag and Drop your photos")
label.grid(row=0, column=0,)


out_label = ttk.Label(text="Output path and desired file name:", font=OUT_LABEL_FONT)
out_label.grid(row=1, column=0, sticky="w")
output_path = ttk.Entry(root, width=50)
output_path.grid(row=1, column=0, sticky="e")

lb = tk.Listbox(root, height=8)
lb.drop_target_register(DND_FILES)
lb.dnd_bind("<<Drop>>", lambda e: lb.insert(tk.END, e.data))
lb.grid(row=2, column=0, sticky="ew")


text_scroll = ttk.Scrollbar(root, orient="vertical", command=lb.yview)
text_scroll.grid(row=2, column=1, sticky="ns")
lb["yscrollcommand"] = text_scroll.set

btn_su = ttk.Button(root, text="Submit", command=submit)
btn_su.grid(row=3, column=0, sticky="w")

btn_clr = ttk.Button(root, text="Clear", command=clear)
btn_clr.grid(row=3, column=0)

btn_del = ttk.Button(root, text="Delete", command=delete)
btn_del.grid(row=3, column=0, sticky="e")

root.mainloop()
