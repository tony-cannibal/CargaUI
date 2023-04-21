from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
# print(Path.home())


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Balance')
        self.geometry('400x150')
        self.resizable(False, False)

        self.frame_1 = ttk.Frame(self)
        self.frame_1.pack(pady=20)

        self.input_dir = ttk.Entry(self.frame_1)
        self.input_dir.pack(side='left', padx=20, ipadx=8,)  # expand=True)

        self.search = ttk.Button(
            self.frame_1, text="Buscar", command=self.get_file_dir)
        self.search.pack(side='left', padx=20, ipadx=8,)  # expand=True)

        self.label = ttk.Label(self, text="Archivo")
        self.label.pack()

    def get_file_dir(self):
        filetypes = (
            ('Excel files', '*.xlsx'),
        )
        file_dir = fd.askopenfilename(
            title='Open a file',
            initialdir=Path.home(),
            filetypes=filetypes
        )
        print(file_dir)


if __name__ == "__main__":
    app = App()
    app.mainloop()
