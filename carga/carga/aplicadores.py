import pandas as pd


def aplicadores_carga(carga):
    carga_L = list(carga['TMNL_L(Auto)'].unique())
    carga_R = list(carga['TMNL_R(Auto)'].unique())
    carga_pL = list(carga['TMNL_L(Semi-auto)'].unique())
    carga_pR = list(carga['TMNL_R(Semi-auto)'].unique())
    total = carga_R + carga_L + carga_pL + carga_pR
    total_generic = []
    for i in total:
        if i != '':
            if i[0] == 'T':
                total_generic.append(i[:-2])
    total_unique = []
    for i in total_generic:
        if i not in total_unique:
            total_unique.append(i)
    # total_unique = set(total_generic)
    return total_unique


def aplcadores_faltantes(aplicadores, carga):
    # print(aplicadores)
    lista_total = aplicadores['Aplicador'].unique()
    apps_carga = aplicadores_carga(carga)
    missing_apps = {}
    missing_apps['Aplicadores Faltantes'] = []
    for i in apps_carga:
        if i not in lista_total:
            missing_apps['Aplicadores Faltantes'].append(i)
    missing_count = len(missing_apps['Aplicadores Faltantes'])
    result = pd.DataFrame.from_dict(missing_apps)
    return result, missing_count
