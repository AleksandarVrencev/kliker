import time
import pyautogui
import os
import tkinter as tk
from pynput import keyboard
from tkinter import messagebox, filedialog, simpledialog
# row counter
i = 1
# make a list of x and y coordinates and click types
lista = []    
# make a list to store key presses
key_presses = []
# bool to stop recording click binds as L,R,D to be able to record key presses
bool_click_recording = True
def main():
    # make a tkinter window with a button 
    root = tk.Tk()
    root.title('Kliker')
    root.geometry('450x600')
    root.resizable(True, True)

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
                else:
                    binder(i[0], i[1], i[2])
                time.sleep(1)
            # maximize window
            root.deiconify() 
    #
    def clear():
        global i
        # reset row counter
        i = 1
        # clear list
        lista.clear()
        # clear listbox
        listbox.delete(0, tk.END)
        # clear entry boxes
        entry_var.set('')
    #
    def record_keyboard_input():
        global bool_click_recording, i
        #bool_click_recording = False
        if hotkey.get() == 'ctrl':
            listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'ctrl' + ' ' + entry_var.get())
            i += 1
            lista.append([pyautogui.position().x, pyautogui.position().y, 'ctrl' , entry_var.get()])
            bool_click_recording = True
            entry_var.set('')
            root.focus()
        elif hotkey.get() == 'alt':
            listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'alt' + ' ' + entry_var.get())
            i += 1
            lista.append([pyautogui.position().x, pyautogui.position().y, 'alt' , entry_var.get()])
            bool_click_recording = True
            entry_var.set('')
            root.focus()
        elif hotkey.get() == 'shift':
            listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'shift' + ' ' + entry_var.get())
            i += 1
            lista.append([pyautogui.position().x, pyautogui.position().y, 'shift' , entry_var.get()])
            bool_click_recording = True
            entry_var.set('')
            root.focus()
        elif hotkey.get() == 'win':
            listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'win' + ' ' + entry_var.get())
            i += 1
            lista.append([pyautogui.position().x, pyautogui.position().y, 'win' , entry_var.get()])
            bool_click_recording = True
            entry_var.set('')
            root.focus()
        else:
            listbox.insert(tk.END, str(i) + "." + str(pyautogui.position().x) + " " + str(pyautogui.position().y) + " " + 'key' + ' ' + entry_var.get())
            i += 1
            lista.append([pyautogui.position().x, pyautogui.position().y, 'key' , entry_var.get()])
            bool_click_recording = True
            entry_var.set('')
            root.focus()

    # send mouse position and click type to a function that will click on that position
    def binder(mouse_x=0, mouse_y=0, click_type=None, key=None):
        if(click_type == 'left'):
            pyautogui.click(x=mouse_x, y=mouse_y, button='left')
        elif(click_type == 'right'):
            pyautogui.click(x=mouse_x, y=mouse_y, button='right')
        elif(click_type == 'double'):
            pyautogui.doubleClick(x=mouse_x, y=mouse_y, button='left')
        elif(click_type == 'key'):
            pyautogui.typewrite(key)
        elif(click_type == 'ctrl'):
            pyautogui.hotkey('ctrl', key)
        elif(click_type == 'alt'):
            pyautogui.hotkey('alt', key)
        elif(click_type == 'shift'):
            pyautogui.hotkey('shift', key)
        elif(click_type == 'win'):
            pyautogui.hotkey('win', key)

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
                        #print(line)
                    # append line to list
                    # lista.append([int(line[0]), int(line[1]), line[2].strip()])
                    # listbox.insert(tk.END, str(j) + '.' + str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]))
                    j += 1 
                # write success messageaca
                messagebox.showinfo("Load", "File loaded successfully!")
                # close file
                file.close()
                i = j
        except:
            messagebox.showinfo("Warning", "You didn't select a file!")
    #aca
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
        #lista.insert(index, [int(x[0]), int(x[1]), x[2]])
        # increment i
        i += 1

    def bool_falser(self):
        global bool_click_recording
        bool_click_recording = False

    # add button to start the script
    start_button = tk.Button(root, text='Start', command=start)
    start_button.grid(row=0, column=0, sticky='w', ipadx=40.5, padx=10, pady=10)
    # add button to clear the list
    clear_button = tk.Button(root, text='Clear', command=clear)
    clear_button.grid(row=2, column=1, sticky='e', ipadx=39.5)
    # add entry field 
    entry_var = tk.StringVar()
    entry = tk.Entry(root, width=20,textvariable=entry_var)
    entry.grid(row=1, column=1, sticky='e', padx=1, pady=10, ipadx=10)
    # bind entry field to boolean variable in order to stop recording binding L,R,D to their functions
    entry.bind('<FocusIn>', bool_falser)

    # add hotkey dropdown menu to select hotkey like ctrl, alt, shift, etc.
    hotkey = tk.StringVar(root)
    #hotkey.set('ctrl')
    hotkey_menu = tk.OptionMenu(root, hotkey, 'ctrl', 'alt', 'shift', 'win')
    hotkey_menu.grid(row=0, column=1, sticky='w', padx=120)
    # add button for record_keyboard_input() function
    keyboard_input_button = tk.Button(root, text='Keyboard input', command=record_keyboard_input)
    keyboard_input_button.grid(row=0, column=1, sticky='e')
    # add button to save list to a file
    save_button = tk.Button(root, text='Save', command=save)
    save_button.grid(row=1, column=0, sticky='w', ipadx=40.5, padx=10, pady=10)
    # add button to load list from a file
    load_button = tk.Button(root, text='Load', command=load)
    load_button.grid(row=2, column=0, sticky='w', ipadx=40, padx=10)
    # make a listbox
    listbox = tk.Listbox(root, width=50, height=20)
    listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    # edit items in listbox with double click on item in listbox 
    listbox.bind('<Double-Button-1>', edit)   
    # start record_mouse_position() function when key is pressed
    #root.bind('<space>', record_mouse_position)
    root.bind('<l>', L)
    root.bind('<r>', R)
    root.bind('<d>', D)
    # make a mainloop for tkinter window
    root.mainloop()

main()