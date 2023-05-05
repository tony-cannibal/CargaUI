import pandas as pd
import mariadb
# from . import functions as fn


exceptions = ['JKT23BULB1B1', 'JWS00EFFL100']
desfMed = ['desforre med', 'sello desforre med']


def prensasInfo(prensas, terminal, lote, circuito):
    res = prensas[
        (prensas["Terminal de union"] == terminal)
        & (prensas["No.circuito"] == circuito)
        & (prensas["LOT"] == lote)
    ].values.tolist()
    if res:
        res = res[0]
        return res[12], res[-1], res[11]
    else:
        return "", "", ""


def app(maquina, terminal, apps):
    res = apps[
        (apps["Almacen"] == maquina) & (apps["Aplicador"] == terminal[0:10])
    ].values.tolist()
    if res:
        return True
    else:
        return False


def procesos(db: dict):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute("""SELECT * FROM procesos""")
    res = cur.fetchall()
    res = [list(i) for i in res]
    procesos = {}
    for i in res:
        procesos[i[1]] = i[2]
    return procesos


def checkAltura(altura, terminalA, terminalM):
    if terminalA == '' and terminalM == '':
        return 'ok'
    elif altura == 0:
        if terminalA == '':
            if terminalM[0] == 'T':
                return 'err'
            else:
                return 'ok'
        else:
            if terminalA[0] == 'T':
                return 'err'
            else:
                return 'ok'
    else:
        return 'ok'


def midStrip(proc, long, desf1, desf2):
    '''
    Chech all non auto mid strip en return "ok" or "err" wheather they
    comply with the established paramerters for correct non auto mid strips.
    '''
    desfMed = ['desforre med', 'sello desforre med']
    # TODO check length of mid strip
    # total length must not be < 240
    # both distances from each terminal must no be < 115
    if desf1 == '':
        return ''
    if proc in desfMed:
        return ''
    if long < 240:
        return 'err'
    dist2 = long - int(desf1)
    if desf1 < 115 and dist2 < 115:
        return 'err'
    else:
        return 'ok'


def specificStatus(corte, prensas, maquinas, con):
    proc = procesos(con)
    d_corte = corte.to_dict("list")

    d_corte["MaquinaP_L"] = []
    d_corte["ProcesoP_L"] = []
    d_corte["MaquinaP_R"] = []
    d_corte["ProcesoP_R"] = []
    for i in range(len(d_corte["Maquina"])):
        terminalL = d_corte["TMNL_L(Semi-auto)"][i]
        terminalR = d_corte["TMNL_R(Semi-auto)"][i]
        lote = d_corte["LOT"][i]
        circuito = d_corte["Nº de circuito"][i]
        if terminalL == "":
            d_corte["MaquinaP_L"].append("")
            d_corte["ProcesoP_L"].append("")
        else:
            maquina, proceso, subMaterial = prensasInfo(
                prensas, terminalL, lote, circuito
            )
            d_corte["MaquinaP_L"].append(maquina)
            d_corte["ProcesoP_L"].append(proceso)
            if subMaterial != "":
                d_corte["SELLO_L"][i] = subMaterial
        if terminalR == "":
            d_corte["MaquinaP_R"].append("")
            d_corte["ProcesoP_R"].append("")
        else:
            maquina, proceso, subMaterial = prensasInfo(
                prensas, terminalR, lote, circuito
            )
            d_corte["MaquinaP_R"].append(maquina)
            d_corte["ProcesoP_R"].append(proceso)
            if subMaterial != "":
                d_corte["SELLO_R"][i] = subMaterial

    d_corte["appAutoL"] = []
    d_corte["appAutoR"] = []
    d_corte["Grom_L"] = []
    d_corte["Grom_R"] = []
    d_corte["etcState"] = []
    for i in range(len(d_corte["Maquina"])):
        maquina = d_corte["Maquina"][i]
        terminalL = d_corte["TMNL_L(Auto)"][i]
        terminalR = d_corte["TMNL_R(Auto)"][i]
        selloL = d_corte["SELLO_L"][i]
        selloR = d_corte["SELLO_R"][i]
        proceso = proc[d_corte["Etc."][i]]
        if maquina[0] == "S" or maquina[0] == "B":
            d_corte["appAutoL"].append("")
            d_corte["appAutoR"].append("")
            d_corte["Grom_L"].append("")
            d_corte["Grom_R"].append("")
        else:
            d_corte["appAutoL"].append(maquinas[maquina].hasAppStr(terminalL))
            d_corte["appAutoR"].append(maquinas[maquina].hasAppStr(terminalR))
            d_corte["Grom_L"].append(
                maquinas[maquina].hasGromStr(terminalL, selloL, exceptions))
            d_corte["Grom_R"].append(
                maquinas[maquina].hasGromStr(terminalR, selloR, exceptions))
        # add a string method for this
        if maquinas[maquina].hasProcesBool(proceso):
            d_corte["etcState"].append("ok")
        else:
            d_corte["etcState"].append("err")

    d_corte["appPrensaL"] = []
    d_corte["appPrensaR"] = []
    for i in range(len(d_corte["Maquina"])):
        maquinaPL = d_corte["MaquinaP_L"][i]
        terminalL = d_corte["TMNL_L(Semi-auto)"][i][0:10]
        maquinaPR = d_corte["MaquinaP_R"][i]
        terminalR = d_corte["TMNL_R(Semi-auto)"][i]
        if maquinaPL == "":
            d_corte["appPrensaL"].append("")
        else:
            d_corte["appPrensaL"].append(
                maquinas[maquinaPL].hasAppStr(terminalL))
        if maquinaPR == "":
            d_corte["appPrensaR"].append("")
        else:
            d_corte["appPrensaR"].append(
                maquinas[maquinaPR].hasAppStr(terminalR))

    d_corte["alturasL"] = []
    d_corte["alturasR"] = []
    for i in range(len(d_corte["Maquina"])):
        alturaL = d_corte['C/H(L)'][i]
        terminalAL = d_corte["TMNL_L(Auto)"][i]
        terminalML = d_corte["TMNL_L(Semi-auto)"][i]
        d_corte['alturasL'].append(
            checkAltura(alturaL, terminalAL, terminalML))

        alturaR = d_corte['C/H(R)'][i]
        terminalAR = d_corte["TMNL_R(Auto)"][i]
        terminalMR = d_corte["TMNL_R(Semi-auto)"][i]
        d_corte['alturasR'].append(
            checkAltura(alturaR, terminalAR, terminalMR))

    d_corte["DesfMed"] = []
    for i in range(len(d_corte["Maquina"])):
        desf1 = d_corte['Desforre en medio 1'][i]
        desf2 = d_corte['Desforre en medio 2'][i]
        longitud = d_corte['Longitud'][i]
        proceso = proc[d_corte["Etc."][i]]
        d_corte['DesfMed'].append(midStrip(proceso, longitud, desf1, desf2))

    o_corte = pd.DataFrame.from_dict(d_corte)

    o_corte = o_corte.reindex(
        columns=[
            'Prioridad', 'LOT', 'Cantidad', 'Materia', 'SQ', 'Color',
            'Longitud', 'C/H(L)', 'alturasL', 'C/H(R)', 'alturasR',
            'TMNL_L(Auto)', 'appAutoL', 'TMNL_R(Auto)', 'appAutoR', 'Etc.',
            'etcState', 'Nº de circuito', 'Maquina', 'Desforre en medio 1',
            'Desforre en medio 2', 'DesfMed', 'MaquinaP_L',
            'TMNL_L(Semi-auto)', 'appPrensaL', 'ProcesoP_L', 'MaquinaP_R',
            'TMNL_R(Semi-auto)', 'appPrensaR', 'ProcesoP_R', 'SELLO_L',
            'Grom_L', 'SELLO_R', 'Grom_R', 'W_CODE', 'P/N'])
    return o_corte
