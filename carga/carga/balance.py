import pandas as pd
import mariadb
from . import functions as fn


def turnos(db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute('SELECT * FROM turnos;')
    res = cur.fetchall()
    turnos = dict(res)
    return turnos


def balance(maquinas, carga, tipo, area, con):
    turnosLocal = turnos(con)
    mList = fn.maquinasList(maquinas, tipo, area)
    err_maq = []

    for i in carga['Maquina'].unique():
        if i not in maquinas:
            err_maq.append(i)

    columns = [
        'Maquinas', 'UPH', 'Capacidad A', 'Capacidad B',
        'Capacidad Total', 'Input', 'Diff'
    ]
    status = {}
    for i in columns:
        status[i] = []

    for i in range(len(mList)):
        status['Maquinas'].append(mList[i])
        status['UPH'].append(maquinas[mList[i]].uph)
        status['Capacidad A'].append(status['UPH'][i] * turnosLocal['A'])
        status['Capacidad B'].append(status['UPH'][i] * turnosLocal['B'])
        status['Capacidad Total'].append(
            status['Capacidad A'][i] + status['Capacidad B'][i])
        status['Input'].append(
            carga[carga['Maquina'] == mList[i]]['Cantidad'].sum())
        if status['Input'][i] == 0:
            status['Diff'].append(0)
        else:
            status['Diff'].append(status['Capacidad Total']
                                  [i] - status['Input'][i])

    dStatus = pd.DataFrame.from_dict(status)
    return dStatus
