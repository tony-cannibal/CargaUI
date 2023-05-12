import mariadb
from .maquinas import Maquina


def trimAuto(df):
    columns = [2, 21, 22]
    df.drop(df.columns[columns], axis=1, inplace=True)
    df = df.fillna("")
    df.rename(
        columns={"TMNL_L(Semi-auto).1": "TMNL_R(Semi-auto)"}, inplace=True)
    # df.to_excel('corte.xlsx', index=False)
    return df


def trimApps(df):
    columns = [1, 4, 5, 6, 7, 8]
    df.drop(df.columns[columns], axis=1, inplace=True)
    df.rename(
        columns={
            "Codigo de barra del aplicador": "Codigo",
            "Codigo del aplicador": "Aplicador",
        },
        inplace=True,
    )
    return df


def trimPrensas(df):
    columns = [0, 4, 5]
    if not df.empty:
        df.drop(df.columns[columns], axis=1, inplace=True)
    return df

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def getApps(df):
    maquinas = df["Almacen"].unique()
    listOfApps = df.values.tolist()
    apps = {}
    for m in maquinas:
        apps[m] = []
        for i in range(len(listOfApps)):
            if listOfApps[i][2] == m:
                apps[m].append(listOfApps[i][1])
    return apps


def getGroms(db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute("""SELECT * FROM grometeras""")
    res = cur.fetchall()
    res = [list(i) for i in res]
    maquinas = [i[4] for i in res]
    maquinas = sorted(set(maquinas))
    grometeras = {}
    for m in maquinas:
        grometeras[m] = []
        for i in range(len(res)):
            if res[i][4] == m:
                grometeras[m].append(res[i][2])
    cur.close()
    return grometeras


def getMaquinas(db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute("""SELECT * FROM maquinas""")
    res = cur.fetchall()
    res = [list(i) for i in res]
    maqs = [i[0] for i in res]
    maquinas = {}
    for i in range(len(maqs)):
        maquinas[maqs[i]] = res[i]
    cur.close()
    return maquinas


def createMaquinas(apps, db):
    # con = mariadb.connect(**db)
    apps = getApps(apps)
    grom = getGroms(db)
    maqs = getMaquinas(db)
    maquinas = {}
    for i in maqs:
        maquina = maqs[i]
        aplicadores = []
        if i in apps:
            aplicadores = apps[i]
        grometeras = []
        if i in grom:
            grometeras = grom[i]
        maquinas[i] = Maquina(maquina, aplicadores, grometeras)
    return maquinas

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def turnos(db):
    con = mariadb.connect(**db)
    cur = con
    cur.execute("SELECT * FROM turnos;")
    res = cur.fetchall()
    turnos = dict(res)
    return turnos


def tiemposDeCambio(db):
    con = mariadb.connect(**db)
    cur = con.cursor()
    cur.execute("SELECT * FROM tiempo_cambio;")
    res = cur.fetchall()
    tCambio = dict(res)
    return tCambio


def maquinasList(maquinas: dict, tipo: str, area: str) -> list:
    mList = []
    for i in maquinas:
        maquina = maquinas[i]
        if maquina.tipo == tipo and area in maquina.area:
            mList.append(maquina.nombre)
    return mList
