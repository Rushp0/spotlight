import tkinter as tk

#TODO: add scroll bar for long definitions

class definition_display:

    def __init__(self, word, entry, main_root):
        self.main_root = main_root
        self.entry = entry
        self.destroy_existing_displays()
        self.root = tk.Toplevel()
        self.root.geometry('700x0+383+210')
        self.root.wm_attributes('-topmost', 1)
        self.root.configure(background='#121212')
        self.root.wm_attributes('-alpha', 0.9)
        self.root.overrideredirect(True)
        self.definition = None
        self.word = word

        self.get_definition()

    def show_definition_display(self):
        self.root.mainloop()

    def update_root(self):
        self.destroy_existing_displays()

    def get_definition(self):
        from PyDictionary import PyDictionary
        dictionary = PyDictionary()
        try:
            self.definition = dictionary.meaning(self.word) # finds definition of word passed
        except ValueError:
            self.entry.set('Invalid Word')
            self.main_root.update()
            self.main_root.after(2000, self.entry.set(''))
            self.root.destroy()
            return

        if 'Adjective' in self.definition:
            self.configure_adjective_display()
        if 'Noun' in self.definition:
            self.configure_noun_display()
        if 'Verb' in self.definition:
            self.configure_verb_display()
        if 'Adverb' in self.definition:
            self.configure_adverb_display()

    def destroy_existing_displays(self):
        for widget in self.main_root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def configure_adjective_display(self):
        def_list = []

        adjective_label = tk.Label(self.root, text='Adjective:', background='#121212', foreground='#b1b5b7',
                                   font='Times_New_Roman 12')
        adjective_label.pack(side='left', anchor='nw')
        for index in range(len(self.definition.get('Adjective'))):  # loops through each definition
            adjective_def = self.definition.get('Adjective')[index]  # gets the definition
            # creates list of label object with the definition
            def_list.append(
                tk.Label(self.root, text=str(index + 1) + ": " + adjective_def, background='#121212', foreground='#b1b5b7',
                         font='Times_New_Roman 12'))

        for label in def_list:  # loops through each definition label
            label.pack(side='top', anchor='sw')  # packs each definition label

        # re-sizes output window height with respect to the number of definitions
        self.root.geometry(f'700x{len(self.definition.get("Adjective")) * 25}+383+210')

    def configure_noun_display(self):
        def_list = []

        noun_label = tk.Label(self.root, text='Noun:', background='#121212', foreground='#b1b5b7',
                              font='Times_New_Roman 12')
        noun_label.pack(side='left', anchor='nw')
        for index in range(len(self.definition.get('Noun'))):
            noun_def = self.definition.get('Noun')[index]
            def_list.append(
                tk.Label(self.root, text=str(index + 1) + ": " + noun_def, background='#121212', foreground='#b1b5b7',
                         font='Times_New_Roman 12'))

        for label in def_list:
            label.pack(side='top', anchor='sw')

        self.root.geometry(f'700x{len(self.definition.get("Noun")) * 25}+383+210')

    def configure_verb_display(self):
        def_list = []

        verb_label = tk.Label(self.root, text='Verb:', background='#121212', foreground='#b1b5b7',font='Times_New_Roman 12')
        verb_label.pack(side='left', anchor='nw')
        for index in range(len(self.definition.get('Verb'))):
            verb_def = self.definition.get('Verb')[index]
            def_list.append(
                tk.Label(self.root, text=str(index + 1) + ": " + verb_def, background='#121212', foreground='#b1b5b7',
                         font='Times_New_Roman 12'))

        for label in def_list:
            label.pack(side='top', anchor='sw')

        self.root.geometry(f'700x{len(self.definition.get("Verb")) * 25}+383+210')

    def configure_adverb_display(self):
        def_list = []

        adverb_label = tk.Label(self.root, text='Adverb:', background='#121212', foreground='#b1b5b7',font='Times_New_Roman 12')
        adverb_label.pack(side='left', anchor='nw')
        for index in range(len(self.definition.get('Adverb'))):
            adverb_def = self.definition.get('Adverb')[index]
            def_list.append(
                tk.Label(self.root, text=str(index + 1) + ": " + adverb_def, background='#121212', foreground='#b1b5b7',
                         font='Times_New_Roman 12'))

        for label in def_list:
            label.pack(side='top', anchor='sw')

        self.root.geometry(f'700x{len(self.definition.get("Adverb")) * 25}+383+210')