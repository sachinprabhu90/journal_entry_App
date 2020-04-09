from tkinter import Tk, Button, Text, Menu, Toplevel
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import geocoder
import os
import logging
import json
logging.basicConfig(filename='logfile.log',level=logging.DEBUG)
# logging.disable(level=logging.CRITICAL)


class Journal():
    def __init__(self, master):

        with open('config.json', 'r') as file:
            self.config = json.load(file)

        master.title('My Journal')
        master.configure(background=self.config['master'])
        master.resizable(False, False)

        # TODO
        # add checklist

        style = ttk.Style()
        style.configure('TEntry',
                        foreground=self.config['entry']['foreground'],
                        fieldbackground=self.config['entry']['background'],
                        font=(self.config['entry']['font'],
                              self.config['entry']['font_size']
                              )
                        )
        style.configure('main.TLabel',
                        background=self.config['label']['background'],
                        foreground=self.config['label']['foreground'],
                        font=(self.config['label']['font'],
                              self.config['label']['font_size']
                              )
                        )

        ttk.Label(master, text='Location: ', style='main.TLabel').grid(
            row=1, column=0, padx=2, pady=3)
        
        self.location_entry = ttk.Entry(master, width=100)
        self.location_entry.grid(row=1, column=2, padx=2, pady=3)

        self.refresh_location_button = HoverButton(master, text="Refresh",
                                                   background=self.config['button']['background'],
                                                   foreground=self.config['button']['foreground'],
                                                   command=lambda: self.refresh_location())
        self.refresh_location_button.grid(row=1, column=3,  padx=2, pady=3)

        # self.text_frame = ttk.Frame(master, width=100, height=100)
        # self.text_frame.grid(row=2, column=0, columnspan=2)

        self.text_entry = Text(
            master, height=30, wrap='word',
            background=self.config['text_field']['background'],
            foreground=self.config['text_field']['foreground'],
            font=(self.config['text_field']['font'],
                  self.config['text_field']['font_size'])

        )

        self.text_entry.grid(row=2, column=0, columnspan=4,
                             sticky='NESW', padx=2, pady=5)

        self.submit_button = HoverButton(master, text="Submit",
                                         background=self.config['button']['background'],
                                         foreground=self.config['button']['foreground'],
                                         command=lambda: self.submit())

        self.submit_button.grid(
            row=3, column=0, sticky='NE', padx=2, pady=5)

        self.clear_button = HoverButton(master, text="Clear",
                                        background=self.config['button']['background'],
                                        foreground=self.config['button']['foreground'],
                                        command=lambda: self.clear())
        self.clear_button.grid(row=3, column=1, sticky='NW', padx=10, pady=5)

        self.about_button = HoverButton(master, text="About",
                                        background=self.config['button']['background'],
                                        foreground=self.config['button']['foreground'],
                                        command=lambda: self.show_help())
        self.about_button.grid(row=3, column=2, sticky='NE', padx=10, pady=5)

        self.customise_button = HoverButton(master, text="Customise Colors",
                                            background=self.config['button']['background'],
                                            foreground=self.config['button']['foreground'],
                                            command=lambda: self.customize(master))
        self.customise_button.grid(
            row=3, column=3, sticky='NE', padx=10, pady=5)

        menubar = Menu(master)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(
            label='    Submit', command=lambda: self.submit(), accelerator='Ctrl+Enter')
        filemenu.add_separator()
        filemenu.add_command(
            label='    Exit', command=lambda: master.quit(), accelerator='Ctrl+X')
        menubar.add_cascade(label='File', menu=filemenu)

        master.config(menu=menubar)

        self.refresh()
        # self.refresh_location()

        # keyboard bindings
        master.bind('<Control-Return>', lambda e: self.submit())
        master.bind('<Control-x>', lambda e: master.quit())
        self.text_entry.focus()

    def refresh(self):
        self.text_entry.delete(1.0, 'end')
        self.text_entry.insert(1.0, 'Journal Entry Here!')

    def refresh_location(self):
        g = geocoder.ip('me')
        logging.debug(print(g))
        self.location_entry.delete(0, 'end')
        if g:
            self.location_entry.insert(0,
                                       f'{g.city} lat:{g.latlng[0]} lng:{g.latlng[1]}'
                                       )
        else:
            self.location_entry.insert(0, 'Enter location')

    def submit(self):
        text = self.text_entry.get(1.0, 'end')
        self.string_text = f"datetime : {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}\nlocation : {self.location_entry.get()}\nentry: {text}\n"
        self.save_to_file()
        self.clear()

    def save_to_file(self):
        self.filename = filedialog.asksaveasfilename(
            filetypes=(("Text File", "*.txt"),))
        logging.debug(type(self.filename))
        logging.debug(self.filename)

        if isinstance(self.filename, str):
            with open(self.filename, 'a') as file:
                logging.debug(f'wrote {self.string_text} to {self.filename}')
                file.write(self.string_text)
            messagebox.showinfo(
                title='Info', message=f'saved to {self.filename}')
        else:
            pass

    def clear(self):
        self.refresh()
        self.location_entry.delete(0, 'end')
        self.text_entry.delete(1.0, 'end')

    def show_help(self):
        messagebox.showinfo(title='Help',
                            message='My Journal helps you to arrange your journal entries along with timestamp and\
                location. Once you submit, new journal entry will be appended to the file selected.\
                \n\nLocation is fetched based on the IP.')

    def customize(self, master):
        self.cust_window = Toplevel(master)
        self.cust_window.config(background=master['background'])
        self.cust_window.bind('<Return>', lambda e: self.write_config())

        ttk.Label(self.cust_window, text='Main Background:',
                  style='main.TLabel').grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Entry Background:',
                  style='main.TLabel').grid(
            row=1, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Entry Foreground:',
                  style='main.TLabel').grid(
            row=2, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Label Background:',
                  style='main.TLabel').grid(
            row=3, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Label Foreground:',
                  style='main.TLabel').grid(
            row=4, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Button Background:',
                  style='main.TLabel').grid(
            row=5, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Button Foreground:',
                  style='main.TLabel').grid(
            row=6, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Journal Entry Background:',
                  style='main.TLabel').grid(
            row=7, column=0, padx=2, pady=2)
        ttk.Label(self.cust_window, text='Journal Entry Foreground:',
                  style='main.TLabel').grid(
            row=8, column=0, padx=2, pady=2)

        self.main_background = ttk.Entry(self.cust_window)
        self.entry_background = ttk.Entry(self.cust_window)
        self.entry_foreground = ttk.Entry(self.cust_window)
        self.label_background = ttk.Entry(self.cust_window)
        self.label_foreground = ttk.Entry(self.cust_window)
        self.button_background = ttk.Entry(self.cust_window)
        self.button_foreground = ttk.Entry(self.cust_window)
        self.journal_background = ttk.Entry(self.cust_window)
        self.journal_foreground = ttk.Entry(self.cust_window)

        self.main_background.grid(row=0, column=1)
        self.entry_background.grid(row=1, column=1)
        self.entry_foreground.grid(row=2, column=1)
        self.label_background.grid(row=3, column=1)
        self.label_foreground.grid(row=4, column=1)
        self.button_background.grid(row=5, column=1)
        self.button_foreground.grid(row=6, column=1)
        self.journal_background.grid(row=7, column=1)
        self.journal_foreground.grid(row=8, column=1)

        # self.submit_config = ttk.Button(self.cust_window, text='Submit', command=lambda:self.write_config())
        self.submit_config = HoverButton(self.cust_window, text="Submit",
                                         background=self.config['button']['background'],
                                         foreground=self.config['button']['foreground'],
                                         command=lambda: self.write_config())
        self.submit_config.grid(row=9, column=0)

        self.populate_entries()

    def write_config(self):
        self.config['master'] = self.main_background.get()
        self.config['entry']['background'] = self.entry_background.get()
        self.config['entry']['foreground'] = self.entry_foreground.get()
        self.config['label']['background'] = self.label_background.get()
        self.config['label']['foreground'] = self.label_foreground.get()
        self.config['button']['background'] = self.button_background.get()
        self.config['button']['foreground'] = self.button_foreground.get()
        self.config['text_field']['background'] = self.journal_background.get()
        self.config['text_field']['foreground'] = self.journal_foreground.get()

        with open('config.json', 'w') as file:
            json.dump(self.config, file)
        messagebox.showinfo(
            title='Info', message='Please restart the application for the changes to take effect')
        self.cust_window.quit()

    def populate_entries(self):
        self.clear_entries()
        self.main_background.insert(0, self.config['master'])
        self.entry_background.insert(0, self.config['entry']['background'])
        self.entry_foreground.insert(0, self.config['entry']['foreground'])
        self.label_background.insert(0, self.config['label']['background'])
        self.label_foreground.insert(0, self.config['label']['foreground'])
        self.button_background.insert(0, self.config['button']['background'])
        self.button_foreground.insert(0, self.config['button']['foreground'])
        self.journal_background.insert(
            0, self.config['text_field']['background'])
        self.journal_foreground.insert(
            0, self.config['text_field']['foreground'])

    def clear_entries(self):
        self.main_background.delete(0, 'end')
        self.entry_background.delete(0, 'end')
        self.entry_foreground.delete(0, 'end')
        self.label_background.delete(0, 'end')
        self.label_foreground.delete(0, 'end')
        self.button_background.delete(0, 'end')
        self.button_foreground.delete(0, 'end')
        self.journal_background.delete(0, 'end')
        self.journal_foreground.delete(0, 'end')


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


def main():
    root = Tk()
    Journal(root)
    root.mainloop()


if __name__ == '__main__':
    main()
