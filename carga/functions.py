import pandas as pd
import constants as cn


def getDate(df):
    data = df['10400']
    f = str(data.iloc[1]['LOT'])
    year = f[2:4]
    month = f[4]
    day = f[5:7]

    date = f'20{year}-{cn.months[month]}-{day}'
    return date


def getRank(df):
    data = df['10400']
    p = str(data.iloc[1]['Prioridad'])[:2]
    if p[1] == '0':
        return p[0]
    else:
        return p


def getArea(df):
    pass


def readFile(file: str):
    '''Read the excel data file and return dataframes for each sheet in
    in the file along with basic information such as date area and priority.
    '''
    df = pd.read_excel(file, sheet_name=None)
    info = file.split('/')[-1].split('.')[0].split(' ')
    # fecha = info[0]
    # prioridad = info[1][1:]
    area = info[2]
    prioridad = getRank(df)
    fecha = getDate(df)
    return df, fecha, prioridad, area


def basic_status(errors) -> dict:
    '''
    Return a dictionary with the general total number of
    errors found.
    '''
    raw = errors.to_dict("list")
    result = {}
    result['Aplicadores'] = sum(raw['AppAutoL']) + sum(raw['AppAutoR'])
    result['Proceso'] = sum(raw['Proceso'])
    result['Grometeras'] = sum(raw['GromL']) + sum(raw['GromR'])
    result['Alturas'] = sum(raw['Alturas L']) + sum(raw['Alturas R'])
    result['Desf Medio'] = sum(raw['DesfMedio'])
    return result
