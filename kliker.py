import time
import pyautogui
import os
import tkinter as tk
from pynput import keyboard
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
import keyboard
# row counter
i = 1
# make a list of x and y coordinates and click types
lista = []    
# make a list to store key presses
key_presses = []
# bool to stop recording click binds as L,R,D to be able to record key presses
bool_click_recording = True
entry_var = ""
list_of_moves = []
def main():
    # make a tkinter window with a button 
    root = tk.Tk()
    root.title('Kliker')
    root.geometry('500x500')
    root.resizable(False, False)
    hotkey = tk.StringVar(root)
    # make a function that will click on all positions in the list
    def start():
        if listbox.size() == 0:
            messagebox.showinfo('Kliker', 'No clicks recorded!')
        else:
            # minimize window
            root.iconify()
            for i in lista:
                if i[2] == 'key' or i[2] == 'ctrl' or i[2] == 'alt' or i[2] == 'shift' or i[2] == 'win':
                    binder(i[0], i[1], i[2], i[3])
                elif i[2] == 'record':
                    binder(i[0], i[1], i[2], i[3])
                else:
                    binder(i[0], i[1], i[2])
                time.sleep(1)
            # maximize window
            root.deiconify() 

    # make a function that will clear the list
    def clear():
        global i, entry_var
        # reset row counter
        i = 1
        # clear list
        lista.clear()
        # clear listbox
        listbox.delete(0, tk.END)
        # clear entry boxes
        entry_var = ""
    
    # make a function that will record keyboard input
    keys_list = ['ctrl', 'alt', 'shift', 'win']
    
    def record_keyboard_input():
        global bool_click_recording, i, entry_var, list_of_moves
        if entry_var == "a":
            messagebox.showinfo('Kliker', 'Enter text!')
        else:
            # every item in the list except the last one
            for r in list_of_moves:
                for c in r[:-1:2]:                    
                    listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + str(c).split("(")[1].split(")")[0])
                    i += 1
                    lista.append([pyautogui.position().x, pyautogui.position().y, 'key' , str(c)[14:15]])
                    bool_click_recording = True
                    entry_var = ""
                    root.focus()
            list_of_moves.clear()
            if hotkey.get() in keys_list:
                listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + hotkey.get() + ' ' + entry_var)
                i += 1
                lista.append([pyautogui.position().x, pyautogui.position().y, hotkey.get() , entry_var])
                bool_click_recording = True
                entry_var = ""
                root.focus()
            else:
                listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'key' + ' ' + entry_var)
                i += 1
                lista.append([pyautogui.position().x, pyautogui.position().y, 'key' , entry_var])
                bool_click_recording = True
                entry_var = ""
                root.focus()
        hotkey.set('Hotkeys')
    click_type_list = ['ctrl', 'alt', 'shift', 'win']
    # send mouse position and click type to a function that will click on that position
    def binder(mouse_x=0, mouse_y=0, click_type=None, key=None):
        if click_type in click_type_list:
            pyautogui.hotkey(click_type, key)
        elif(click_type == 'left'):
            pyautogui.click(x=mouse_x, y=mouse_y, button='left')
        elif(click_type == 'right'):
            pyautogui.click(x=mouse_x, y=mouse_y, button='right')
        elif(click_type == 'double'):
            pyautogui.doubleClick(x=mouse_x, y=mouse_y, button='left')
        elif(click_type == 'key'):
            pyautogui.typewrite(key)

    # write save function that will save list to a file
    def save():
        if listbox.size() == 0:
            messagebox.showinfo("Error", "No data to save!")
        else:
            # ask user for file name with filedialog
            try:
                file_name = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
                # display warning if user didn't enter a file name
                if not file_name or file_name == '':
                    messagebox.showinfo("Info", "No file name given!")
                else:
                    # open file
                    file = open(file_name, 'w')
                    # write list to file
                    for i in lista:
                        if i[2] == 'key':
                            file.write(str(i[0]) + "," + str(i[1]) + "," + i[2] + "," + i[3] + '\n')
                        else:
                            file.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n')
                    # close file
                    file.close()
                    # write success message
                    messagebox.showinfo("Save", "File saved successfully!")
            except:
                messagebox.showinfo("Warning", "Something went wrong!")

    # write load function that will load list from a file
    def load():
        global i
        clear()
        j = 1
        # ask user for file name with filedialog
        try:
            file_name = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            # display warning if user didn't enter a file name
            if not file_name or file_name == '':
                messagebox.showinfo("Warning", "You didn't select a file!")
            else:
                # open file
                file = open(file_name, 'r')
                # read file
                for line in file:
                    # split line
                    line = line.split(',')
                    if line[2] == 'key':
                        listbox.insert(tk.END, str(j) + "." + line[0] + " " + line[1] + " " + line[2] + " " + line[3])
                        lista.append([int(line[0]), int(line[1]), line[2].strip(), line[3].strip()])
                        #print(line)
                    else:
                        listbox.insert(tk.END, str(j) + "." + line[0] + " " + line[1] + " " + line[2])
                        lista.append([int(line[0]), int(line[1]), line[2].strip()])
                    j += 1 
                # write success messageaca
                messagebox.showinfo("Load", "File loaded successfully!")
                # close file
                file.close()
                i = j
        except:
            messagebox.showinfo("Warning", "You didn't select a file!")
    # functions that bind the L,R and D buttons to mouse recording function
    def L(self):
        global i, bool_click_recording
        if bool_click_recording:
            mouse_position = pyautogui.position()
            lista.append([mouse_position.x, mouse_position.y, 'left'])
            listbox.insert(tk.END, str(i) + '.' + str(mouse_position.x) + " " + str(mouse_position.y) + " " + 'left')
            i += 1
    def R(self):
        global i, bool_click_recording
        if bool_click_recording:
            mouse_position = pyautogui.position()
            lista.append([mouse_position.x, mouse_position.y, 'right'])
            listbox.insert(tk.END, str(i) + '.' +  str(mouse_position.x) + " " + str(mouse_position.y) + " " + 'right')
            i += 1
    def D(self):
        global i, bool_click_recording
        if bool_click_recording:
            mouse_position = pyautogui.position()
            lista.append([mouse_position.x, mouse_position.y, 'double'])
            listbox.insert(tk.END, str(i) + '.' +  str(mouse_position.x) + " " + str(mouse_position.y) + " " + 'double')
            i += 1

    # write function to edit items in listbox
    def edit(event):
        global i
        # get index of selected item
        index = listbox.curselection()[0]
        # get value of selected item
        value = listbox.get(index)
        # delete selected item
        listbox.delete(index)
        # save value to variable
        edit_value = lista[index]
        # delete selected item from list
        lista.pop(index)
        # decrement i
        i -= 1
        # insert new item in listbox
        listbox.insert(index, simpledialog.askstring("Edit", "Edit item", initialvalue=value))
        # insert new item in list
        x = listbox.get(index)[2:].split(' ')
        print(x)
        if edit_value[2] == 'key':
            lista.insert(index, [int(x[0]), int(x[1]), x[2], x[3]])
        else:
            lista.insert(index, [int(x[0]), int(x[1]), x[2]])
        # increment i
        i += 1

    # write function to take text input from user
    def printer():
        global entry_var
        entry_var = simpledialog.askstring('Text', 'Enter text: ')

    # add delete function to delete item from listbox 
    def delete():
        if listbox.curselection():
            # get index of selected item
            index = listbox.curselection()[0]
            # delete selected item
            listbox.delete(index)
            # delete selected item from list
            lista.pop(index)
            # decrement i
            global i
            #i -= 1
            # loop through listbox items and renumber them 
            for i in range(listbox.size()):
                listbox.delete(i)
                listbox.insert(i, str(i+1) + '.' + str(lista[i][0]) + " " + str(lista[i][1]) + " " + lista[i][2])
                i += 2
        else:
            messagebox.showinfo("Warning", "You didn't select an item!")
    # write help function that will display help message to user 
    def help():
        messagebox.showinfo("Help", "Welcome to the help section!\n\nTo record mouse clicks, press the L for left click, R for right click and D for double click.\
        \n\nTo type text press entry button, write text and press add button to add text to listbox.\
        \n\nTo record hotkeys like ctrl+s or alt+f4, choose option from hotkey button, press entry button, type a letter and press add button to add choosen combination to listbox.\
        \n\nTo save your list, press the save button.\n\nTo load a list, press the load button.\
        \n\nTo edit an item, double click on it.\n\nTo remove an item, press the remove button.\
        \n\nTo clear the list, press the clear button.\n\nTo start the program, press the start button.\
        \n\nTo exit the program, press the exit button.")
    
    def record():
        global list_of_moves
        # Record events until 'esc' is pressed.
        messagebox.showinfo("Recording", "Press 'esc' to stop recording!")
        # change focus from
        recorded = keyboard.record(until='esc')
        print(recorded)
        list_of_moves.append(recorded)
        play()

    def play():
        for i in list_of_moves:
            keyboard.play(i, speed_factor=1)

    # add file menu to the menu bar with commands
    file_menu = Menu(root, tearoff=0)
    root.config(menu=file_menu)
    file_menu.add_command(label="Start", command=start)
    file_menu.add_command(label="Save", command=save)
    file_menu.add_command(label="Load", command=load)
    file_menu_new = Menu(file_menu, tearoff=0)
    file_menu_new.add_radiobutton(label="Ctrl", variable=hotkey, value='ctrl')
    file_menu_new.add_radiobutton(label="Alt", variable=hotkey, value='alt')
    file_menu_new.add_radiobutton(label="Shift", variable=hotkey, value='shift')
    file_menu_new.add_radiobutton(label="Win", variable=hotkey, value='win')
    file_menu.add_cascade(label="Hotkey", menu=file_menu_new)
    file_menu.add_command(label="Entry", command=printer)
    file_menu.add_command(label="Add", command=record_keyboard_input)
    file_menu.add_command(label="Clear", command=clear)
    file_menu.add_command(label="Remove", command=delete)
    file_menu.add_command(label="Record", command=record)
    file_menu.add_command(label="Help", command=help)
    # make a listbox
    listbox = tk.Listbox(root, width=59, height=20)
    listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    # edit items in listbox with double click on item in listbox 
    listbox.bind('<Double-Button-1>', edit)   
    root.bind('<l>', L)
    root.bind('<r>', R)
    root.bind('<d>', D)
    # make a mainloop for tkinter window
    root.mainloop()

main()