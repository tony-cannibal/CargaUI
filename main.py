from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import carga
import conn
# print(Path.home())


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Balance')
        self.geometry('600x180')
        # self.resizable(False, False)

        self.result = None

        self.file_dir = tk.StringVar(value='archivo')
        self.frame_1 = ttk.Frame(self)
        self.frame_1.pack(pady=20)

        # self.input_dir = ttk.Entry(self.frame_1)
        self.search_bttn = ttk.Button(
            self.frame_1, text="Buscar", command=self.get_file_dir)
        self.search_bttn.pack(side='left', padx=20)  # expand=True)

        self.analyse_bttn = ttk.Button(
            self.frame_1, text='Analizar', command=self.analizar_info)
        self.analyse_bttn.pack(
            expand=True, side='left', padx=20)  # expand=True)

        self.label = ttk.Label(
            self, borderwidth=1, relief="solid", font='arial 10 bold',
            textvariable=self.file_dir, anchor='center')
        self.label.pack(fill="x", padx=40)

        columns = ['Aplicadores', 'Proceso',
                   'Grometeras', 'Alturas', 'Desf Medio']

        self.result_table = ttk.Treeview(
            self, columns=columns, show='headings', height=1)
        self.result_table.heading('Aplicadores', text='Aplicadores')
        self.result_table.column('Aplicadores', width=70, anchor='center')
        self.result_table.heading('Proceso', text='Proceso')
        self.result_table.column('Proceso', width=70, anchor='center')
        self.result_table.heading('Grometeras', text='Grometeras')
        self.result_table.column('Grometeras', width=110, anchor='center')
        self.result_table.heading('Alturas', text='Alturas')
        self.result_table.column('Alturas', width=70, anchor='center')
        self.result_table.heading('Desf Medio', text='Desf Medio')
        self.result_table.column('Desf Medio', width=100, anchor='center')
        self.result_table.pack(padx=20, pady=20, expand=False)

        self.result_table.tag_configure(
            "even", background='white', foreground='black')
        self.result_table.tag_configure(
            "odd", background='light gray', foreground='black')

        self.frame_2 = ttk.Frame(self)
        self.frame_2.pack(pady=20, fill='both', expand=True)

    def get_file_dir(self):
        filetypes = (
            ('Excel files', '*.xlsx'),)
        file = fd.askopenfilename(
            title='Open a file',
            initialdir=Path.home(),
            filetypes=filetypes)
        self.file_dir.set(file)

    def analizar_info(self):
        ruta = self.file_dir.get()
        self.result = carga.analisys(ruta, conn.con, False)
        apps = self.result['Aplicadores']
        proc = self.result['Proceso']
        grom = self.result['Grometeras']
        alt = self.result['Alturas']
        desf = self.result['Desf Medio']
        table_length = len(self.result_table.get_children())
        if table_length > 0:
            for row in self.result_table.get_children():
                self.result_table.delete(row)
            self.result_table.insert(
                '', tk.END, values=(apps, proc, grom, alt, desf),
                tags=('odd',))
        else:
            self.result_table.insert(
                '', tk.END, values=(apps, proc, grom, alt, desf),
                tags=('odd',))


if __name__ == "__main__":
    app = App()
    app.mainloop()
