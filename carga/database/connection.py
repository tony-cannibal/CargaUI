import sqlite3
import pandas as pd


def connection(db):
    con = sqlite3.connect(db)
    return con


def deploydb(con):
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS maquinas (
                    maquina VARCHAR(6) PRIMARY KEY,
                    area VARCHAR(4),
                    subArea VARCHAR(30),
                    tipo VARCHAR(30),
                    uph INT,
                    procesos VARCHAR(30)
                    );''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS turnos (
                    turno VARCHAR(3) PRIMARY KEY,
                    horas REAL
                    );''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS tiempo_cambio (
                    tipo VARCHAR(10) PRIMARY KEY,
                    minutos REAL
                    );''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS grometeras (
                    id INT PRIMARY KEY,
                    kit VARCHAR(16),
                    sello VARCHAR(16),
                    area VARCHAR(4),
                    maquina VARCHAR(6)
                    );''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS procesos (
                    area VARCHAR(20),
                    etc VARCHAR(50),
                    proceso VARCHAR(20)
                );
                ''')
    cur.close()
    con.commit()
    cur.close()
    con.close()


def populateMaquinas(con, data):
    df = pd.read_excel(data)
    df = df.values.tolist()
    cur = con.cursor()
    for i in df:
        cur.execute('''
                    INSERT INTO maquinas (
                        maquina, area, subArea, tipo, uph, procesos
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?
                    );
                    ''', (i[0], i[1], i[2], i[3], i[4], i[5]))
        con.commit()
    cur.close()


def populateGrom(con, data):
    df = pd.read_excel(data)
    df = df.values.tolist()
    cur = con.cursor()
    for i in df:
        cur.execute('''
                    INSERT INTO grometeras (
                        id, kit, sello, area, maquina
                    ) VALUES (
                        ?, ?, ?, ?, ?
                    );''', (i[0], i[1], i[2], i[3], i[4]))
        con.commit()
    cur.close()


def populateProc(con, data):
    df = pd.read_excel(data)
    df = df.values.tolist()
    cur = con.cursor()
    for i in df:
        cur.execute('''
                    INSERT INTO procesos (
                        area, etc, proceso
                    ) VALUES (
                        ?, ?, ?
                    );''', (i[0], i[1], i[2]))
        con.commit()
    cur.close()


def populateTurno(db):
    turnos = [
        ('A', 8.4),
        ('B', 8),
        ('C', 0)
    ]
    cur = db.cursor()
    for i in turnos:
        cur.execute('''
                    INSERT INTO turnos (
                        turno, horas
                    ) VALUES (
                        ?, ?
                    );
                    ''', i)
        db.commit()
    cur.close()


def populateTiempoCambio(db):
    tCambio = [
        ('app', 2),
        ('cable', 2)
    ]
    cur = db.cursor()
    for i in tCambio:
        cur.execute('''
                    INSERT INTO tiempo_cambio (
                        tipo, minutos
                    ) VALUES (
                        ?, ?
                    );
                    ''', i)
        db.commit()
    cur.close()


def populatedb(con, maquinas, grometeras, procesos):
    populateMaquinas(con, maquinas)
    populateGrom(con, grometeras)
    populateProc(con, procesos)
    populateTiempoCambio(con)
    populateTurno(con)


if __name__ == "__main__":
    pass
    # populatedb(connection(database), data)
