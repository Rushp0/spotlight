import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from PIL import Image, ImageTk
import threading, json, logging

def start_listener():
    logging.info("Starting hot key listener")
    with keyboard.GlobalHotKeys({
        '<f9>': lambda : start(),
        '<ctrl>+c': lambda: save_to_clipboard()
    }) as listener:
        listener.join()

def start():
    s = spotlight()
    s.start()

def save_to_clipboard():
    from tkinter import Tk

    if len(spotlight.clips) == 10: # keeps the last 10 clips
        logging.info("clip cap reached")
        spotlight.clips.pop(0) # removes the clip at the first index
        spotlight.clipboard_history_file.truncate(0) # clears file
        for clip in spotlight.clipboard_history_file:
            spotlight.clipboard_history_file.write(clip.strip()+'\n') # rewrites clips

    spotlight.clipboard_history_file.readline(0)
    spotlight.clips.append(Tk().clipboard_get().strip()) # append new clip to list
    spotlight.clipboard_history_file.write(Tk().clipboard_get().strip() + '\n') # appends new clips to file
    spotlight.clipboard_history_file.flush() # flushes file to save it)

class spotlight:

    clips = []
    clipboard_history_file = open(r'C:\Users\rushi\PycharmProjects\Spotlight\spotlight\clipboard_history.txt', 'a+')

    def __init__(self):
        self.command_list, self.autocomplete_list = ['Google', 'Map', 'Define', 'Clipboard', 'Chrome', 'Documents', 'Pycharm',
                'Trash', 'Spotify', 'Mail', 'Weather', 'Directions', 'Command Prompt'], []
        self.ac_icon_list, self.ac_label_list = [], []
        self.index_tab, self.index_scroll = 0, 0

        # opens data file which contains icon file paths
        with open(r'C:\Users\rushi\PycharmProjects\Spotlight\data', 'r') as read_file:
            self.data = json.load(read_file)

        self.bookmarks = {}
        # get bookmarks in chrome
        bookmarks_file = json.load(open(r'C:\Users\rushi\AppData\Local\Google\Chrome\User Data\Default\Bookmarks'))

        for bookmark in bookmarks_file.get('roots').get('bookmark_bar').get('children'):
            self.bookmarks[bookmark.get('name')] = bookmark.get('url')
            self.command_list.append(bookmark.get('name'))
        self.command_list.sort(reverse=True)

        import pyautogui
        pyautogui.click(515,190)

        self.root = tk.Tk()
        self.root.geometry('700x35+383+175')
        self.root.wm_attributes('-topmost', 1)
        self.root.configure(background='#121212')
        self.root.wm_attributes('-alpha',0.9)
        self.root.overrideredirect(True)

        # entry config
        self.input_text = tk.StringVar()
        self.entry = tk.Entry(self.root, width=70, textvariable=self.input_text, font='system 20', background='#121212',
                              foreground='#b1b5b7', borderwidth=0, highlightthickness=0)
        self.entry.pack()
        self.entry.focus_force()

        #bindings
        self.root.bind('<FocusOut>', lambda d: self.root.destroy())
        self.root.bind('<Escape>', lambda d: self.root.destroy())
        self.root.bind('<End>', lambda a: self.partial_autocomplete('end'))
        self.root.bind('<Key>', lambda a: self.partial_autocomplete('none'))
        self.root.bind('<Tab>', lambda a: self.partial_autocomplete('tab'))
        self.root.bind('<Up>', lambda s: self.scroll_autocomplete('up'))
        self.root.bind('<Down>', lambda s: self.scroll_autocomplete('down'))
        self.root.bind('<BackSpace>', lambda u: self.update_autocomplete())
        self.root.bind('<Return>', lambda p: self.pass_input())

        # shows root window
        self.root.mainloop()

    def pass_input(self):
        from results import results
        results(self.root, self.input_text)
    def pass_input_click(self, text):
        from results import results
        self.input_text.set(text.strip())
        results(self.root, self.input_text)

    def partial_autocomplete(self, action):
        # if end is pressed from pyautogui, doesnt do anything
        # this prevents the autocomplete list from updating
        if action == 'end':
            return
        # sets text in entry when pressing tab
        if action == 'tab':
            if self.index_tab >= len(self.autocomplete_list): # resets index of autocomplete list if the index goes over
                self.index_tab = 0                            # length of the autocomplete list
            self.input_text.set(self.autocomplete_list[self.index_tab])
            self.index_tab += 1
            import pyautogui
            pyautogui.press('end') # makes typing faster
            return

        self.autocomplete_list = []
        for command in self.command_list:
            # add command to top of list if the first letters match to make autocomplete better
            if self.input_text.get().capitalize() == command[0:len(self.input_text.get())].capitalize() and (not len(self.input_text.get()) == 0):
                self.autocomplete_list.insert(0, command) # inserts command to top of list
                continue
            # if the command contains the entered text it gets added to the autocomplete list
            if self.input_text.get().lower() in command.lower() and (not len(self.input_text.get()) == 0):
                self.autocomplete_list.append(command)
        self.clear_icons() # clears icons that are placed

        self.ac_icon_list, self.ac_label_list = [], []
        if not len(self.autocomplete_list) == 0: # makes sure there are commands to autocomplete
            for command in self.autocomplete_list: # loops through command list
                # important: bookmarks are stored in favicon file - a sql lite file
                icon_path = self.data.get('icons').get(command.lower()) # get icon path from data.json
                temp_image = (ImageTk.PhotoImage(Image.open(icon_path).resize((20,20)))) # creates image
                self.ac_icon_list.append(temp_image)

                temp_label = (tk.Label(self.root, text="  "+command, image=temp_image, background='#121212',
                                               font='verdana 13', compound=tk.LEFT, foreground='#dedede', width=675,
                                               anchor='w',height=25))
                self.ac_label_list.append(temp_label)

                temp_label.bind('<Button-1>', self.helper1(temp_label)) # click-able label
                temp_label.bind('<Enter>', self.helper2(temp_label)) # hover feature
                temp_label.bind('<Leave>', self.helper3(temp_label))

                temp_label.pack(anchor='w',padx=(10,0), pady=1) # packs labels

        self.root.geometry(f'700x{len(self.ac_label_list)*34+35}') # change size of window based on length of command list

    def scroll_autocomplete(self, direction):
        # resets index to 0 if length is greater than the length of autocomplete list
        if self.index_scroll >= len(self.autocomplete_list)-1 or self.index_scroll == -len(self.autocomplete_list):
            self.index_scroll = 0
        if not len(self.input_text.get()) == 0: # checks if there is input
            if direction == 'down':
                self.index_scroll += 1
            else:
                self.index_scroll -= 1
            # replaces text in entry
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.autocomplete_list[self.index_scroll])

    def clear_icons(self): # clears the icons that are showing in the drop down
        for label in self.ac_label_list:
            label.pack_forget()

    def clicked(self, txt): # sets entry text to label that was clicked
        self.entry.delete(0, tk.END)
        self.entry.insert(0, txt.strip())

    def update_autocomplete(self):
        self.autocomplete_list = []
        self.index_tab = 0
        self.clear_icons()
        self.partial_autocomplete('key')
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    @staticmethod
    def start(): # starts listening for f9
        start_listener()
    def helper1(self, label): # helps bind click on label
        return lambda x: self.clicked(label.cget('text'))
    @staticmethod
    def helper2(label): # helps bind Enter to change color
        return lambda x: label.config(bg='#4f4f4f')
    @staticmethod
    def helper3(label): # helps bind Leave to change of color
        return lambda x: label.config(bg='#121212')

import ctypes
ctypes.windll.user32.MessageBoxW(0, "Starting", "Starting", 0)
listener_thread = threading.Thread(target=start_listener)
print("Starting")
listener_thread.start()