import pandas as pd


def errores(carga):
    maquinas = carga['Maquina'].unique()

    cols = ['Maquina', 'AppAutoL', 'AppAutoR', 'Proceso', 'GromL',
            'GromR', 'Alturas L', 'Alturas R', 'DesfMedio']

    resumen = {}
    for i in cols:
        resumen[i] = []

    for i in maquinas:
        resumen['Maquina'].append(i)
        resumen['AppAutoL'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['appAutoL'] == 'err')]['Nº de circuito'].count())
        resumen['AppAutoR'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['appAutoR'] == 'err')]['Nº de circuito'].count())
        resumen['Proceso'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['etcState'] == 'err')]['Nº de circuito'].count())
        resumen['GromL'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['Grom_L'] == 'err')]['Nº de circuito'].count())
        resumen['GromR'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['Grom_R'] == 'err')]['Nº de circuito'].count())
        resumen['Alturas L'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['alturasL'] == 'err')]['Nº de circuito'].count())
        resumen['Alturas R'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['alturasR'] == 'err')]['Nº de circuito'].count())
        resumen['DesfMedio'].append(
            carga[(carga['Maquina'] == i) &
                  (carga['DesfMed'] == 'err')]['Nº de circuito'].count())

    o_resumen = pd.DataFrame.from_dict(resumen)
    return o_resumen
