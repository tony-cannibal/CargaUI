import pandas as pd
from .functions import maquinasList
from .functions import tiemposDeCambio


def appChange(index, current, previous):
    if index == 0:
        if current != '':
            return 1
        else:
            return 0
    else:
        if current != '':
            if current != previous:
                return 1
            else:
                return 0
        else:
            return 0


def check_cable(index, current, previous):
    if index == 0:
        return 1
    if current != previous:
        return 1
    else:
        return 0


def cambios(df, maqs, area, con):
    maquinas = maquinasList(maqs, 'corte', area)
    tiempos = tiemposDeCambio(con)
    carga = df.to_dict("list")

    cols = ['Maquina', 'UPH', 'Cable', 'App L',
            'App R', 'Tiempo', 'Minutos x Hora', 'Velocidad']
    cambios = {}
    for i in cols:
        cambios[i] = []

    for m in maquinas:
        cambios['Maquina'].append(maqs[m].nombre)
        cambios['UPH'].append(maqs[m].uph)
        cable_total = 0
        appL_total = 0
        appR_total = 0
        for i in range(len(carga['Maquina'])):
            if m == carga['Maquina'][i]:
                # cable
                cable_a = carga['W_CODE'][i]
                cable_p = carga['W_CODE'][i - 1]
                cable_c = check_cable(i, cable_a, cable_p)
                cable_total += cable_c
                # aplicador L
                appL_a = carga['TMNL_L(Auto)'][i]
                appL_p = carga['TMNL_L(Auto)'][i - 1]
                appL_c = appChange(i, appL_a, appL_p)
                appL_total += appL_c
                # aplicador R
                appR_a = carga['TMNL_R(Auto)'][i]
                appR_p = carga['TMNL_R(Auto)'][i - 1]
                appR_c = appChange(i, appR_a, appR_p)
                appR_total += appR_c

        cambios['Cable'].append(cable_total)
        cambios['App L'].append(appL_total)
        cambios['App R'].append(appR_total)

    for i in range(len(maquinas)):
        tAppTotal = (cambios['App L'][i] +
                     cambios['App R'][i]) * tiempos['app']
        tCableTotal = cambios['Cable'][i] * tiempos['cable']
        cambios['Tiempo'].append(tAppTotal + tCableTotal)

        minuto_hora = round(cambios['Tiempo'][i] / 16.4, 2)
        cambios['Minutos x Hora'].append(minuto_hora)

        if cambios['Minutos x Hora'][i] == 0:
            cambios['Velocidad'].append(0)
        else:
            uph = cambios['UPH'][i]
            setup = cambios['Minutos x Hora'][i]
            vel = round((uph / (60 - setup)) * 60, 2)
            cambios['Velocidad'].append(vel)

    cambios = pd.DataFrame.from_dict(cambios)
    return cambios
