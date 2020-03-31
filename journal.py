from tkinter import *
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import geocoder
import os
import logging
logging.basicConfig(level=logging.DEBUG)
# logging.disable(level=logging.CRITICAL)


class Journal():
    def __init__(self, master):
        master.title('My Journal')

        # TODO
        # create new journal - Done
        # add checklist

        style = ttk.Style()
        style.configure('TEntry', foreground='blue',
                        background='grey', font=('Arial', 20))
        style.configure('TButton', foreground='blue',
                        background='LightBlue3', font=('Arial', 12))
        style.configure('TLabel', foreground='blue', font=('Arial', 12))

        ttk.Label(master, text='Date & Time: ').grid(
            row=0, column=0, padx=2, pady=3)
        self.datetime_entry = ttk.Entry(
            master, state=DISABLED, style='entry.TEntry')
        self.datetime_entry.grid(row=0, column=1, padx=2, pady=3)
        self.refresh_button = ttk.Button(
            master, text='Refresh', command=lambda: self.refresh())
        self.refresh_button.grid(row=0, column=2, padx=2, pady=3)

        ttk.Label(master, text='Location: ').grid(
            row=1, column=0, padx=2, pady=3)
        self.location_entry = ttk.Entry(master, style='entry.TEntry')
        self.location_entry.grid(row=1, column=1, padx=2, pady=3)
        self.refresh_location_button = ttk.Button(
            master, text='Refresh', command=lambda: self.refresh_location())
        self.refresh_location_button.grid(row=1, column=2,  padx=2, pady=3)

        # self.text_frame = ttk.Frame(master, width=100, height=100)
        # self.text_frame.grid(row=2, column=0, columnspan=2)

        self.text_entry = Text(
            master, height=30, foreground='blue', font=('Time New Roman', 15))
        self.text_entry.grid(row=2, column=0, columnspan=3,
                             sticky='NESW', padx=2, pady=5)

        self.submit_button = ttk.Button(
            master, text='Submit', command=lambda: self.submit())
        self.submit_button.grid(
            row=3, column=0, columnspan=3, sticky='NESW', padx=2, pady=5)

        self.refresh()

    def refresh(self):
        self.datetime_entry.config(state=NORMAL)
        self.datetime_entry.delete(0, 'end')
        self.datetime_entry.insert(
            0, datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
        self.datetime_entry.config(state=DISABLED)

    def refresh_location(self):
        g = geocoder.ip('me')
        self.location_entry.delete(0, 'end')
        self.location_entry.insert(0, g.city)

    def submit(self):
        text = self.text_entry.get(1.0, 'end')
        self.string_text = f"datetime : {self.datetime_entry.get()}\nlocation : {self.location_entry.get()}\nentry: {text}\n"
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


def main():
    root = Tk()
    Journal(root)
    root.mainloop()


if __name__ == '__main__':
    main()
