from tkinter import *
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import geocoder
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logging.disable(level=logging.CRITICAL)


class Journal():
    def __init__(self, master):
        master.title('My Journal')
        master.configure(background = '#ADABC3')

        # TODO
        # add checklist

        style = ttk.Style()
        style.configure('TEntry', foreground='#354160', disabledfieldbackground = '#ADABC3',
                        fieldbackground='#ADABC3', font=('Arial', 20))
        style.configure('TButton', foreground='#354160',
                        background='#ADABC3', font=('Arial', 12))
        style.configure('TLabel', background = '#ADABC3',foreground='#354160', font=('Arial', 12))

        ttk.Label(master, text='Date & Time: ').grid(
            row=0, column=0, padx=2, pady=3)
        self.datetime_entry = ttk.Entry(
            master, state=DISABLED, style='entry.TEntry', width=100)
        self.datetime_entry.grid(row=0, column=1, padx=2, pady=3)
        self.refresh_button = ttk.Button(
            master, text='Refresh', command=lambda: self.refresh())
        self.refresh_button.grid(row=0, column=2, padx=2, pady=3)

        ttk.Label(master, text='Location: ').grid(
            row=1, column=0, padx=2, pady=3)
        self.location_entry = ttk.Entry(
            master, style='entry.TEntry', width=100)
        self.location_entry.grid(row=1, column=1, padx=2, pady=3)
        self.refresh_location_button = ttk.Button(
            master, text='Refresh', command=lambda: self.refresh_location())
        self.refresh_location_button.grid(row=1, column=2,  padx=2, pady=3)

        # adding tabs above text
        tab = ttk.Notebook(master)
        tab.grid(row=2,column = 0,columnspan = 50,rowspan = 49,sticky='NESW')
        tab1 = ttk.Frame(tab,style='My.TFrame')
        tab.add(tab1,text='Tab1')

 
        nb = ttk.Notebook(tab1)
        page1 = ttk.Frame(nb)
        nb.add(page1,text='Scanning')

        rows=0
        while rows < 50:
            tab1.rowconfigure(rows,weight=1)
            tab1.columnconfigure(rows,weight=1)
            rows+=1

        page2 = ttk.Frame(nb)
        nb.add(page2,text='Imagine')
        
        page3 = ttk.Frame(nb)
        nb.add(page3,text='Impurity')
        
        page4 = ttk.Frame(nb)
        nb.add(page4,text='Marking')

        # self.text_entry = Text(
        #     master, height=30, background = '#ADABC3',foreground='#354160', font=('Time New Roman', 15))
        # self.text_entry.grid(row=2, column=0, columnspan=3,
        #                      sticky='NESW', padx=2, pady=5)

        self.submit_button = ttk.Button(
            master, text='Submit', command=lambda: self.submit())
        self.submit_button.grid(
            row=3, column=0, columnspan=3, sticky='NESW', padx=2, pady=5)

        self.refresh()
        self.refresh_location()

        # keyboard bindings
        master.bind('<Return>', lambda e: self.submit())

    def refresh(self):
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
            messagebox.showinfo(title='location',
                                message=f'Location Refreshed\nCity:{g.city}\nlatlang:{g.latlng}'
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


def main():
    root = Tk()
    Journal(root)
    root.mainloop()


if __name__ == '__main__':
    main()