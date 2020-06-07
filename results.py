import webbrowser as wb
import subprocess, logging

class results:

    def __init__(self, root, input_text):

        self.entry = input_text
        self.input_text = input_text.get().strip().lower()
        self.root = root

        self.bookmarks = {}
        self.get_chrome_bookmarks()

        # if input is only one word, ie command w/o parameters
        # contains special cases
        if self.input_text == 'google drive' or self.input_text == 'command prompt' or\
                self.input_text.title() in self.bookmarks or self.input_text.find(' ') == -1:
            logging.info("Has no parameters")
            self.command = None
        else:
            self.command = self.input_text[0:self.input_text.find(' ')].lower()
            logging.info("Has parameters")
        # checks if input text is just a command or command with parameters
        if self.command:
            self.has_parameters()
        else:
            self.command_only()

    def has_parameters(self):
        if self.command == 'def' or self.command == 'define':
            logging.info("Called Define")
            import definition_display
            word = self.input_text[self.input_text.find(' ') + 1:]
            d = definition_display.definition_display(word, self.entry, self.root)  # creates definition gui
            d.show_definition_display()  # shows display for definition
        # google search
        elif self.command == 'google':
            logging.info("Called google search")
            wb.open_new_tab('www.google.com/search?q=+' + (''.join(self.input_text[6:])))
            self.root.destroy()
        # map a given address
        elif self.command == 'map':
            logging.info("Called map")
            wb.open_new_tab('https://www.google.com/maps/search/'+ (''.join(self.input_text[4:])))
            self.root.destroy()
        # get directions; origin is home
        elif self.command == 'dir' or self.command == 'directions' or self.command == 'direction':
            logging.info("Called directions")
            wb.open_new_tab('https://www.google.com/maps/dir/?api=1&origin=164+kossuth+st+piscataway+nj+08854&destination='+
                            self.input_text[self.input_text.find(' ') + 1:])
            self.root.destroy()
        else:
            logging.info("Invalid Input: " + self.input_text)
            self.entry.set("Invalid Input")
            self.root.update()
            self.root.after(2000, self.entry.set(''))
            print('Invalid Input')

    def command_only(self):
        import re

        website_regex = re.compile(r'www\.[A-Za-z0-9]{1,20}\.(com|net|gov|edu)') # regex for website w/ www.
        website_regex_no_www = re.compile(r'[A-Za-z0-9]{1,20}\.com|net|gov|edu') # regex for website w/o www.

        # important: comparisons must be lowercase
        if self.input_text == 'google drive':
            logging.info("Opening Google Drive")
            wb.open_new_tab('https://drive.google.com/drive/u/0/my-drive')
            self.root.destroy()
        elif self.input_text == 'chrome':
            logging.info("Opening Chrome")
            subprocess.Popen('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
            self.root.destroy()
        elif self.input_text == 'documents':
            logging.info("Opening Documents folder")
            subprocess.Popen(r'explorer /open, C:\Users\rushi\Desktop\Documents')
            self.root.destroy()
        elif self.input_text == 'pycharm':
            logging.info("Opening Pycharm")
            subprocess.Popen(r'C:\Program Files\JetBrains\PyCharm Community Edition 2019.3.3\bin\pycharm64.exe')
            self.root.destroy()
        elif self.input_text == 'spotify':
            logging.info("Opening spotify")
            subprocess.Popen(r'C:\Users\rushi\AppData\Roaming\Spotify\Spotify.exe')
            self.root.destroy()
        elif self.input_text == 'mail':
            logging.info("Opening mail")
            wb.open_new_tab('https://mail.google.com')
            self.root.destroy()
        elif self.input_text == 'cmd' or self.input_text == 'command prompt':
            logging.info("Opening cmd")
            subprocess.Popen(r'C:\Users\rushi\AppData\Local\Microsoft\WindowsApps\wt.exe')
            self.root.destroy()
        elif self.input_text == 'trash':
            print('t')
            logging.info("Opening Trash")
            subprocess.Popen(r'explorer /open,  C:\Users\rushi\Desktop')
            self.root.destroy()
        elif self.input_text.title() in self.bookmarks:
            logging.info("Opening from chrome bookmarks")
            wb.open_new_tab(self.bookmarks.get(self.input_text.title()))
            self.root.destroy()
        elif self.input_text == 'weather':
            logging.info("called weather")
        elif self.input_text == 'clipboard':
            logging.info("called clipboard")
        elif website_regex.search(self.input_text) or website_regex_no_www.search(self.input_text):
            logging.info("Opening website"+ self.input_text)
            if self.input_text[0:3].lower() == 'www':
                wb.open_new_tab(self.input_text)
            else: wb.open_new_tab('www.'+self.input_text)
        else:
            logging.info("Invalid Input: "+self.input_text)
            self.entry.set("Invalid Input")
            self.root.update()
            self.root.after(2000, self.entry.set(''))

    def get_chrome_bookmarks(self):
        import json
        # loads data file
        bookmarks_file = json.load(open(r'C:\Users\rushi\AppData\Local\Google\Chrome\User Data\Default\Bookmarks'))
        for bookmark in bookmarks_file.get('roots').get('bookmark_bar').get('children'):
            # add bookmarks to bookmark dictionary
            self.bookmarks[bookmark.get('name')] = bookmark.get('url')