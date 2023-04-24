import pandas as pd


def getDate(df):
    pass


def getRank(df):
    pass


def getArea(df):
    pass


def readFile(file):
    '''Read the excel data file and return dataframes for each sheet in
    in the file along with basic information such as date area and priority.
    '''
    df = pd.read_excel(file, sheet_name=None)
    info = file.split('/')[-1].split('.')[0].split(' ')
    fecha = info[0]
    prioridad = info[1][1:]
    area = info[2]
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
