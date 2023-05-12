from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import carga
import conn
import constants as cn
# print(Path.home())


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Balance')
        self.geometry('610x780')
        # self.resizable(False, False)

        self.result = None
        self.balance = None
        self.area = None
        self.prioridad = None
        self.fecha = None

        self.file_dir = tk.StringVar(value='archivo')
        self.save_res = tk.BooleanVar(value=False)

        self.frame_1 = ttk.Frame(self)
        self.frame_1.pack(pady=25)

        # self.input_dir = ttk.Entry(self.frame_1)
        self.search_bttn = ttk.Button(
            self.frame_1, text="Buscar", command=self.get_file_dir)
        self.search_bttn.pack(side='left', padx=20)  # expand=True)

        self.analyse_bttn = ttk.Button(
            self.frame_1, text='Analizar', command=self.analizar_info)
        self.analyse_bttn.pack(
            expand=True, side='left', padx=20)

        self.save_result = ttk.Checkbutton(
            self.frame_1, text='Guardar', variable=self.save_res,
            onvalue=True, offvalue=False)
        self.save_result.pack(
            expand=True, side='left', padx=20)

        self.label = ttk.Label(
            self, borderwidth=1, relief="solid", font='arial 10 bold',
            textvariable=self.file_dir, anchor='center', background='white')
        self.label.pack(fill="x", padx=40, pady=10)

        self.sep_1 = ttk.Separator(self, orient='horizontal')
        self.sep_1.pack(fill='x', padx=40, pady=25)
    ###########################################################################
        self.master_1 = ttk.Frame(self)
        self.master_1.pack(pady=10)

        # Area
        self.frame_area = ttk.Frame(self.master_1)
        self.frame_area.pack(side='left', padx=10)
        self.area_title = ttk.Label(
            self.frame_area, text='Area', font='arial 12 bold underline')
        self.area_title.pack(side='left', padx=5)
        self.label_area = ttk.Label(
            self.frame_area, text='    ', font='arial 12 ',
            background='white', borderwidth=1, relief="solid")
        self.label_area.pack(side='left')

        # Prioridad
        self.frame_prioridad = ttk.Frame(self.master_1)
        self.frame_prioridad.pack(side='left', padx=10)
        self.prioridad_title = ttk.Label(
            self.frame_prioridad, text='Prioridad',
            font='arial 12 bold underline')
        self.prioridad_title.pack(side='left', padx=5)
        self.label_prioridad = ttk.Label(
            self.frame_prioridad, text='     ', font='arial 12 ',
            background='white', borderwidth=1, relief="solid")
        self.label_prioridad.pack(side='left')

        # Fecha
        self.frame_fecha = ttk.Frame(self)
        self.frame_fecha.pack(pady=10)
        self.fecha_title = ttk.Label(
            self.frame_fecha, text='Fecha', font='arial 12 bold underline')
        self.fecha_title.pack(side='left', padx=5)
        self.label_fecha = ttk.Label(
            self.frame_fecha, text='     ', font='arial 12 ',
            background='white', borderwidth=1, relief="solid")
        self.label_fecha.pack(side='left')

        self.table_label_1 = ttk.Label(
            self, text="Errores", font="arial 12 bold")
        self.table_label_1.pack(pady=5)

        self.result_table = ttk.Treeview(
            self, columns=cn.columns, show='headings', height=1)
        # self.result_table.heading('Aplicadores', text='Aplicadores')
        # self.result_table.column('Aplicadores', width=70, anchor='center')
        self.result_table.heading('Proceso', text='Proceso')
        self.result_table.column('Proceso', width=70, anchor='center')
        self.result_table.heading('Grometeras', text='Grometeras')
        self.result_table.column('Grometeras', width=110, anchor='center')
        self.result_table.heading('Alturas', text='Alturas')
        self.result_table.column('Alturas', width=70, anchor='center')
        self.result_table.heading('Desf Medio', text='Desf Medio')
        self.result_table.column('Desf Medio', width=100, anchor='center')
        self.result_table.heading('Apps Falt.', text='Apps Falt.')
        self.result_table.column('Apps Falt.', width=80, anchor='center')
        self.result_table.pack(padx=20, pady=0, expand=False)
        self.result_table.tag_configure(
            "even", background='white', foreground='black')
        self.result_table.tag_configure(
            "odd", background='light gray', foreground='black')

        self.table_label_2 = ttk.Label(
            self, text="Balance", font="arial 12 bold")
        self.table_label_2.pack(pady=5)

        self.frame_2 = ttk.Frame(self)
        self.frame_2.pack(pady=5)
        self.balance_table = ttk.Treeview(
            self.frame_2, columns=['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            show='headings', height=15)
        self.balance_table.heading('a', text=cn.columns2[0])
        self.balance_table.column('a', width=70, anchor='center')
        self.balance_table.heading('b', text=cn.columns2[1])
        self.balance_table.column('b', width=60, anchor='center')
        self.balance_table.heading('c', text=cn.columns2[2])
        self.balance_table.column('c', width=80, anchor='center')
        self.balance_table.heading('d', text=cn.columns2[3])
        self.balance_table.column('d', width=80, anchor='center')
        self.balance_table.heading('e', text=cn.columns2[4])
        self.balance_table.column('e', width=100, anchor='center')
        self.balance_table.heading('f', text=cn.columns2[5])
        self.balance_table.column('f', width=60, anchor='center')
        self.balance_table.heading('g', text=cn.columns2[6])
        self.balance_table.column('g', width=60, anchor='center')
        self.balance_table.pack(side='left')
        self.balance_table.tag_configure(
            "even", background='white', foreground='black')
        self.balance_table.tag_configure(
            "odd", background='light gray', foreground='black')
        self.balance_table.tag_configure(
            "bad", background='#fa9393', foreground='black')

        self.balance_yscroll = ttk.Scrollbar(
            self.frame_2, orient='vertical', command=self.balance_table.yview)
        self.balance_yscroll.pack(side='right', fill='y')
        self.balance_table.configure(yscrollcommand=self.balance_yscroll.set)

    ###########################################################################

    def get_file_dir(self) -> None:
        '''Get file'''
        filetypes = (
            ('Excel files', '*.xlsx'),)
        file = fd.askopenfilename(
            title='Open a file',
            initialdir=f"{Path.home()}/Documents",
            filetypes=filetypes)
        self.file_dir.set(file)

    def populate_res_table(self) -> None:
        # apps = self.result['Aplicadores']
        proc = self.result['Proceso']
        grom = self.result['Grometeras']
        alt = self.result['Alturas']
        desf = self.result['Desf Medio']
        m_apps = self.result['Missing Apps']
        table_length = len(self.result_table.get_children())
        if table_length > 0:
            for row in self.result_table.get_children():
                self.result_table.delete(row)
            self.result_table.insert(
                '', tk.END, values=(proc, grom, alt, desf, m_apps),
                tags=('odd',))
        else:
            self.result_table.insert(
                '', tk.END, values=(proc, grom, alt, desf, m_apps),
                tags=('odd',))

    def populate_balance_table(self):
        table_length = len(self.balance_table.get_children())
        if table_length > 0:
            for row in self.balance_table.get_children():
                self.balance_table.delete(row)
        length = len(self.balance['Maquinas'])
        # self.balance_table.config(height=length)
        for i in range(length):
            maquina = self.balance['Maquinas'][i]
            uph = self.balance['UPH'][i]
            cap_a = self.balance['Capacidad A'][i]
            cap_b = self.balance['Capacidad B'][i]
            cap_total = self.balance['Capacidad Total'][i]
            input = self.balance['Input'][i]
            diff = self.balance['Diff'][i]
            if diff < 0:
                self.balance_table.insert(
                    '', tk.END,
                    values=(maquina, uph, cap_a, cap_b,
                            cap_total, input, diff), tags='bad')
            elif (i + 1) % 2 == 0:
                self.balance_table.insert(
                    '', tk.END,
                    values=(maquina, uph, cap_a, cap_b,
                            cap_total, input, diff), tags='even')
            else:
                self.balance_table.insert(
                    '', tk.END, values=(maquina, uph, cap_a, cap_b,
                                        cap_total, input, diff), tags='odd')

    def analizar_info(self) -> None:
        ruta = self.file_dir.get()
        if ruta == "" or ruta == "archivo":
            pass
        else:
            res = carga.analisys(
                ruta, conn.con, self.save_res.get())
            self.result = res[0]
            self.balance = res[1]
            self.area = res[2]
            self.prioridad = res[3]
            self.fecha = res[4]
            self.label_area.config(text=f' {self.area.upper()} ')
            self.label_prioridad.config(text=f' {self.prioridad} ')
            self.label_fecha.config(text=f' {self.fecha} ')
            self.populate_res_table()
            self.populate_balance_table()


if __name__ == "__main__":
    app = App()
    app.mainloop()
