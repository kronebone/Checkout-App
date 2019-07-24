"""
A program that stores user data and handles equipment checkouts:
Stored user Data is Name, email, phone number, total equipment checkouts

Operations include:

Interact with user records:
View all entries
Search entries
Update entry
Delete entry

Create equipment checkout file
Export users database information
"""

from tkinter import *
from tkinter import ttk
from string import punctuation
from time import strftime
import checkout_backend as cdb
import checkout_config as cfg



window = Tk()
window.title('Equipment Checkout')
window.resizable(0, 0)

# box label frame and labels for database info
user_frame = ttk.LabelFrame(window, text=" User Info - Searchable by any field")
user_frame.grid(row=0, column=0, pady=5)

l_name = Label(user_frame, text='Name:')
l_name.grid(row=0, column=0)

l_phone = Label(user_frame, text='Phone:')
l_phone.grid(row=1, column=0)

l_email = Label(user_frame, text='Email:')
l_email.grid(row=0, column=2)

l_checkouts = Label(user_frame, text='Past checkouts:')
l_checkouts.grid(row=1, column=2)

l_checkouts_num = Label(user_frame, text=' - ')
l_checkouts_num.grid(row=1, column=3)

# database text/entry boxes
name_text = StringVar()
e_name = Entry(user_frame, textvariable=name_text)
e_name.grid(row=0, column=1)

phone_text = StringVar()
e_phone = Entry(user_frame, textvariable=phone_text)
e_phone.grid(row=1, column=1)

email_text = StringVar()
e_email = Entry(user_frame, textvariable=email_text)
e_email.grid(row=0, column=3)

# labelframe for db display and buttons
db_frame = ttk.LabelFrame(window, text="")
db_frame.grid(row=1, column=0, padx=5, pady=5)

l_enable_edit = Label(db_frame, text='Edit mode is:')
l_enable_edit.grid(row=6, column=0)


# functions for buttons
def allow_edit():
    b_enable_edit.configure(text='Enabled', command=disallow_edit)
    b_delete_record['state'] = 'active'
    b_add['state'] = 'active'
    b_update['state'] = 'active'


def disallow_edit():
    b_enable_edit.configure(text='Disabled', command=allow_edit)
    b_delete_record['state'] = 'disabled'
    b_add['state'] = 'disabled'
    b_update['state'] = 'disabled'


def get_selected_row(event):
    global selected_tuple

    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)

    except IndexError:
        pass

    try:
        e_name.delete(0, END)
        e_name.insert(END, selected_tuple[1])

        e_email.delete(0, END)
        e_email.insert(END, selected_tuple[2])

        e_phone.delete(0, END)
        e_phone.insert(END, selected_tuple[3])

        l_checkouts_num.configure(text=selected_tuple[4])

    except NameError:
        pass

    
def view_command():
    list1.delete(0, END)
    for row in cdb.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in cdb.search(e_name.get(), e_email.get(), e_phone.get()):
        list1.insert(END, row)


def add_command():
    if e_name.get != '{}':
        cdb.insert(e_name.get(), e_email.get(), e_phone.get())
        list1.delete(0, END)
        list1.insert(END, f'{e_name.get()} has been added:')
        for row in cdb.search(e_name.get(), e_email.get(), e_phone.get()):
            list1.insert(END, row)
        disallow_edit()
        list1.select_set(1)
        list1.event_generate("<<ListboxSelect>>")
    else:
        list1.insert(END, 'Check name and try again')


def delete_command():
    cdb.delete(selected_tuple[0])
    e_name.delete(0, END)
    e_email.delete(0, END)
    e_phone.delete(0, END)
    l_checkouts_num.configure(text='-')
    view_command()


def update_command():
    cdb.update(selected_tuple[0], e_name.get(), e_email.get(), e_phone.get())
    list1.delete(0, END)
    list1.insert(END, f'{e_name.get()} has been updated:')
    for row in cdb.search(e_name.get(), e_email.get(), e_phone.get()):
        list1.insert(END, row)


def export_data_command():
    export_date = strftime("%m") + strftime("%d") + strftime("%y")
    total_checkouts = 0
    for row in cdb.view():
        total_checkouts += row[4]

    with open('Checkout Export ' + export_date + '.docx', 'w') as export:
        export.write(f'Total Checkouts: {total_checkouts}' + '\n')
        for row in cdb.view():
            export.write(''.join(str(row).strip(punctuation)) + '\n')
        export.close()
    list1.delete(0, END)
    list1.insert(END, f'Data will be saved as: "Checkout Export {export_date}.docx" upon exiting.')


def cancel_command():
    window.destroy()


def process_checkout_command():
    try:
        cdb.update_total_co(selected_tuple[0], selected_tuple[4])

        checkout_date = strftime("%m") + strftime("%d") + strftime("%y")
        dis = cfg.disclaimer

        with open(str(e_name.get()) + " " + checkout_date + '.docx', 'a') as chkout_list:
            chkout_list.write("\n" + "\n" + str(e_name.get()) + " " + str(e_phone.get()) + "\n" + "\n")
            chkout_list.write("Camera: " + str(cam_type.get()) + ", " + str(cam_amt.get()) + "\n")
            chkout_list.write("Batteries: " + str(battery_amt.get()) + "\n")
            chkout_list.write("Tripod(s): " + str(tripod_amt.get()) + "\n")
            chkout_list.write("Other Gear: " + str(extra_gear_var.get()) + "\n" + "\n")

            chkout_list.write("Signature:__________________________  " + strftime("%x") + "\n")
            chkout_list.write("\n" + "Gear return date:__________" + "Project name:____________________" "\n")
            chkout_list.write("\n" + "Date returned:__________, checked in by:__________" + "\n")
            chkout_list.write("\n" + "Camera usage hours:______" + "\n")
            chkout_list.write("\n" + dis)
            chkout_list.close()

        cancel_command()

    except NameError:
        list1.delete(0, END)
        list1.insert(END, "Please select a user before confirming checkout.")
        pass


#  database buttons
b_enable_edit = Button(db_frame, text='Disabled', command=allow_edit)
b_enable_edit.grid(row=6, column=1)

b_delete_record = Button(db_frame, text="Delete User", command=delete_command)
b_delete_record.grid(row=0, column=2)
b_delete_record['state'] = 'disabled'

b_view_all = Button(db_frame, text='View All', command=view_command)
b_view_all.grid(row=0, column=0, pady=5)

b_search = Button(db_frame, text='Search', command=search_command)
b_search.grid(row=0, column=1, ipadx=10)

b_add = Button(db_frame, text='Add User', command=add_command)
b_add.grid(row=6, column=2)
b_add['state'] = 'disabled'

b_update = Button(db_frame, text='Update User', command=update_command)
b_update.grid(row=6, column=3)
b_update['state'] = 'disabled'

b_save_data = Button(db_frame, text='Export Data', command=export_data_command)
b_save_data.grid(row=0, column=3)

# listbox with scrollbar to display producer database results
scroller = Scrollbar(db_frame)
scroller.grid(row=2, column=4, rowspan=4, sticky=NS)

list1 = Listbox(db_frame, height=10, width=60, yscrollcommand=scroller.set)
list1.grid(row=2, column=0, rowspan=3, columnspan=4)
list1.bind('<<ListboxSelect>>', get_selected_row)

scroller.configure(command=list1.yview)

# equipment checkout label frame and labels
gear_frame = ttk.LabelFrame(window, text=" Gear List ")
gear_frame.grid(row=3, column=0, columnspan=4)

ttk.Label(gear_frame, text="Camera Type:").grid(row=0, column=0)
ttk.Label(gear_frame, text="# of Cameras:").grid(row=0, column=3)
ttk.Label(gear_frame, text="# of Batteries:").grid(row=1, column=3, padx=10)
ttk.Label(gear_frame, text="# of Tripods:").grid(row=1, column=0)
ttk.Label(gear_frame, text="Extra Gear:").grid(row=2, column=0)

# equipment checkout text/entry boxes
cam_type = ttk.Combobox(gear_frame, width=13, values=[x.strip(' ') for x in cfg.camera_types.split(',')], state="readonly")
cam_type.grid(row=0, column=1)

cam_amt = ttk.Combobox(gear_frame, width=13, values=(1, 2, 3))
cam_amt.grid(row=0, column=4)

battery_amt = ttk.Combobox(gear_frame, width=13, values=(1, 2, 3))
battery_amt.grid(row=1, column=4)

tripod_amt = ttk.Combobox(gear_frame, width=13, values=(1, 2, 3))
tripod_amt.grid(row=1, column=1)

extra_gear_var = StringVar()
ttk.Entry(gear_frame, width=46, textvariable=extra_gear_var).grid(row=2, column=1, columnspan=4)

# equipment checkout buttons
b_cancel_exit = Button(gear_frame, text='Exit', command=cancel_command, padx=30)
b_cancel_exit.grid(row=3, column=3)

b_process_checkout = Button(gear_frame, text='Confirm Checkout', command=process_checkout_command)
b_process_checkout.grid(row=3, column=4)

view_command()
window.mainloop()
