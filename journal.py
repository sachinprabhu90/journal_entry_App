from tkinter import *
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import geocoder
import os
import logging
from gradient import GradientFrame
logging.basicConfig(level=logging.DEBUG)
logging.disable(level=logging.CRITICAL)


class Journal():
    def __init__(self, master):
        master.title('My Journal')
        master.configure(background = '#253042')
        master.resizable(False , False)

        # TODO
        # add checklist

        style = ttk.Style()
        style.configure('TEntry', foreground='white',
                        fieldbackground='#253042', font=('Arial', 20))
        # style.map("TEntry",fieldbackground=[("active", "yellow"), ("disabled", "red")])
        style.configure('TButton', foreground='white',
                        background='#253042', font=('Arial', 12))
        style.configure('main.TLabel', background = '#253042',foreground='white', font=('Arial', 12))

        # ttk.Label(master, text='Date & Time: ', style = 'main.TLabel').grid(
        #     row=0, column=0, padx=2, pady=3)
        self.datetime_entry = ttk.Entry(master, state='read_only',  width=100)
        # self.datetime_entry.grid(row=0, column=1, padx=2, pady=3)
        self.refresh_button = ttk.Button(
            master, text='Refresh', command=lambda: self.refresh())
        # self.refresh_button.grid(row=0, column=2, padx=2, pady=3)

        ttk.Label(master, text='Location: ', style='main.TLabel').grid(
            row=1, column=0, padx=2, pady=3)
        self.location_entry = ttk.Entry(master, width=100)
        self.location_entry.grid(row=1, column=1, padx=2, pady=3)
        self.refresh_location_button = HoverButton(master,text="Refresh", 
                                        background='#253042', 
                                        foreground='white', 
                                        command=lambda : self.refresh_location())
        self.refresh_location_button.grid(row=1, column=2,  padx=2, pady=3)

        # self.text_frame = ttk.Frame(master, width=100, height=100)
        # self.text_frame.grid(row=2, column=0, columnspan=2)

        self.text_entry = Text(
            master, height=30, wrap='word', background = '#373B44',foreground='white', font=('Time New Roman', 15))
        
        self.text_entry.grid(row=2, column=0, columnspan=3,
                             sticky='NESW', padx=2, pady=5)
    

        self.submit_button = HoverButton(master,text="Submit", 
                                        background='#253042', 
                                        foreground='white', 
                                        command=lambda : self.submit())

        self.submit_button.grid(
            row=3, column=0, sticky='NE', padx=2, pady=5)


        self.clear_button = HoverButton(master,text="Clear", 
                                        background='#253042', 
                                        foreground='white', 
                                        command=lambda : self.clear())
        self.clear_button.grid(row=3, column=1, sticky='NW', padx=10, pady=5)

        self.about_button = HoverButton(master,text="About", 
                                        background='#253042', 
                                        foreground='white', 
                                        command=lambda : self.show_help())
        self.about_button.grid(row=3, column=2, sticky='NE', padx=10, pady=5)

        self.refresh()
        # self.refresh_location()

        # keyboard bindings
        master.bind('<Control-Return>', lambda e: self.submit())
        self.text_entry.focus()

    def refresh(self):
        self.text_entry.delete(1.0, 'end')
        self.text_entry.insert(1.0, 'Journal Entry Here!')
        self.datetime_entry.config(state=NORMAL)
        self.datetime_entry.delete(0, 'end')
        self.datetime_entry.insert(
            0, datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
        self.datetime_entry.config(state=DISABLED)

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
        self.string_text = f"datetime : {self.datetime_entry.get()}\nlocation : {self.location_entry.get()}\nentry: {text}\n"
        self.save_to_file()
        self.clear()

    def save_to_file(self):
        # messagebox.showinfo(
        # title='Info', message='If you already have a journal entry file select .txt file and your journal entry will be appended\nIgnore the system warning')
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

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
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