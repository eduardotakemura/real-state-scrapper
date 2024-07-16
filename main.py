from tkinter import *
from tkinter import scrolledtext, messagebox, simpledialog
from tkinter import ttk
from scrapper import Scrapper
import math

def start_scrap():
    url = url_input.get()
    fields_config = {
        "type": type_check.get(),
        "price1": price1_check.get(),
        "price2": price2_check.get(),
        "address": address_check.get(),
        "size": size_check.get(),
        "link": link_check.get(),
    }
    entries = int(max_entries.get())
    file_name = file_name_input.get()
    confirm = messagebox.askokcancel(title="Confirmation", message=f"Your inputs were:\n"
                                                                   f"URL to Scrap: {url}\n"
                                                                   f"Entries to Scrap: {entries}\n"
                                                                   f"Name of the result file: {file_name}\n"
                                                                   f"Do you confirm?\n"
                                                                   f"This will take something between "
                                                                   f"{math.ceil(entries/10*0.33)} to {math.ceil(entries/10*1)} minutes.")
    if confirm:
        errors, rows, duration = scrapper.scrap_page(url,file_name,entries,fields_config)
        messagebox.showinfo(title="Confirmation", message=f"Scrap finished!\n"
                                                          f"Your {file_name}.csv data was saved at the scraps folder.\n"
                                                          f"A total of {rows} entries were scrapped, "
                                                          f"occurring {errors} errors.\n"
                                                          f"Total duration: {duration} minutes.")
        url_input.delete(0,END)
        result_label.config(text="")
        url_input.focus_set()

def check_page():
    url = url_input.get()
    scrap = scrapper.get_first_page(url)
    if not scrap:
        messagebox.showwarning("Fail","Sorry, some problem happen when accessing this page, check it and try again.")
    else:
        result_label.config(text=f"The page you've inserted has {scrap} entries.")

# -------- WINDOWS AND GENERAL CONFIG -------- #
window = Tk()
window.title("Scrapper")
window.config(padx=50,pady=50,width=500,height=600)
PAGES_OPTIONS = ["5 Andar"]
page_input_options = StringVar(window)
page_input_options.set(PAGES_OPTIONS[0])
max_entries = StringVar(value="100")
scrapper = Scrapper()
type_check = BooleanVar(value=True)
price1_check = BooleanVar(value=True)
price2_check = BooleanVar(value=True)
address_check = BooleanVar(value=True)
size_check = BooleanVar(value=True)
link_check = BooleanVar(value=True)

# -------- HEADER -------- #
title_label = Label(text="Scrapper APP",font=("Time New Roman",20))
info_label = Label(text="Use this APP to extract (scrap) data from real state pages.\n"
                        "1) First select the page you wish to scrap.\n"
                        "2) Second paste the page URL you want to scrap.\n"
                        "3) Click on the 'Check' button to check if the page is available,\n"
                        "and confirm if it's really the page you want to scrap, \n"
                        "by matching the number of results founds.",font=("Time New Roman",10))

# Positioning #
title_label.grid(column=0,row=0,columnspan=3)
info_label.grid(column=0,row=1,columnspan=3, pady=20)

# -------- INPUT FIELDS -------- #
page_label = Label(text="Select page")
page_input = ttk.Combobox(window, textvariable=page_input_options, values=PAGES_OPTIONS, state="readonly")
url_label = Label(text="URL to Scrap")
url_input = Entry(width=50)
url_check_button = Button(text="Check",command=check_page)
result_label = Label(text="")
url_input.focus_set()

# Positioning #
page_label.grid(column=0,row=2)
page_input.grid(column=1,row=2,columnspan=2,sticky='w')
url_label.grid(column=0,row=3)
url_input.grid(column=1,row=3,sticky='w')
url_check_button.grid(column=2,row=3)
result_label.grid(column=0,row=4,columnspan=3)

# -------- CONFIG FIELDS -------- #
config_title_label = Label(text="Select the fields you want to retrieve",font=("Time New Roman",12,"bold"))
type_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=type_check)
type_label = Label(text='Real State Type')
price1_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=price1_check)
price1_label = Label(text='Price (when Buying) or Total Rent Price (when renting)')
price2_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=price2_check)
price2_label = Label(text='Condo/Expenses (when Buying) or Rent Only Price (when renting)')
address_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=address_check)
address_label = Label(text='Address')
size_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=size_check)
size_label = Label(text='Size (m2), number of dorms')
link_cb = ttk.Checkbutton(window, onvalue=True, offvalue=False, variable=link_check)
link_label = Label(text='Page link')

# Positioning #
config_title_label.grid(column=0,row=5,columnspan=2,pady=10,sticky='w')
type_cb.grid(column=0,row=6)
type_label.grid(column=1,row=6,sticky='w')
price1_cb.grid(column=0,row=7)
price1_label.grid(column=1,row=7,sticky='w')
price2_cb.grid(column=0,row=8)
price2_label.grid(column=1,row=8,sticky='w')
address_cb.grid(column=0,row=9)
address_label.grid(column=1,row=9,sticky='w')
size_cb.grid(column=0,row=10)
size_label.grid(column=1,row=10,sticky='w')
link_cb.grid(column=0,row=11)
link_label.grid(column=1,row=11,sticky='w')

# -------- FILE CONFIG -------- #
file_title_label = Label(text="File Configs",font=("Time New Roman",12,"bold"))
entries_number_label = Label(text='Máx Entries')
entries_spin = ttk.Spinbox(window, from_=0,to=100000,textvariable=max_entries)
warning_entries = Label(text="Each 10 entries processing may take about 20 to 90 seconds, "
                             "increasing as entries increase")
file_name_label = Label(text='File name')
file_name_input = Entry(width=50)
file_name_input.insert(0, "output")

# Positioning #
file_title_label.grid(column=0,row=12,columnspan=2,pady=10,sticky='w')
entries_number_label.grid(column=0,row=13)
entries_spin.grid(column=1,row=13,sticky='w')
warning_entries.grid(column=0,row=14,sticky='w',columnspan=3)
file_name_label.grid(column=0,row=15,pady=5)
file_name_input.grid(column=1,row=15,sticky='w')

# -------- BUTTON AND RESULTS AREA -------- #
confirm_button = Button(text="Scrap!",width=30,command=start_scrap)
scrapping_label = Label(text="")

# Positioning #
confirm_button.grid(column=1,row=16,pady=15)
scrapping_label.grid(column=0,row=17,columnspan=3)

window.mainloop()