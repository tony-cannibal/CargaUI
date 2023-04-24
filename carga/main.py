import pandas as pd
try:
    import carga
    from database import connection as con
    import database
    import functions as fn
except ImportError:
    from . import carga
    from .database import connection as con
    from . import database
    from . import functions as fn

dbase = "carga.db"

data1 = "input/2023-03-28 r1 m1.xlsx"
data2 = "input/2023-03-28 r1 m2.xlsx"


def redeployDb():
    grometeras = "info/grometeras.xlsx"
    maquinas = "info/maquinas.xlsx"
    procesos = "info/procesos.xlsx"
    database.deploydb(con(dbase))
    database.populatedb(con(dbase), maquinas, grometeras, procesos)


def main(file: str, dbase: str, out: bool) -> dict:
    df, fecha, prioridad, area = fn.readFile(file)

    apps = carga.trimApps(df["50160"])
    prensas = carga.trimPrensas(df["10500"])
    auto = carga.trimAuto(df["10400"])
    maquinas = carga.createMaquinas(apps, con(dbase))

    status = carga.specificStatus(auto, prensas, maquinas, con(dbase))
    balanceCorte = carga.balance(maquinas, auto, "corte", area, con(dbase))
    balancePrensas = carga.balance(
        maquinas, prensas, "prensa", area, con(dbase))
    cambios = carga.cambios(auto, maquinas, area, con(dbase))
    errores = carga.errores(status)

    if out:
        path = file[:-5]
        o_file = f"{path} resultado.xlsx"
        with pd.ExcelWriter(o_file) as writer:
            errores.to_excel(writer, sheet_name="resumen", index=False)
            balanceCorte.to_excel(writer, sheet_name="balance", index=False)
            balancePrensas.to_excel(
                writer, sheet_name="balance prensas", index=False)
            status.to_excel(writer, sheet_name="status", index=False)
            cambios.to_excel(writer, sheet_name="cambios", index=False)

    return fn.basic_status(errores)


def say_hello():
    print('Hello')


if __name__ == "__main__":
    result = main(data2, dbase, False)
    print(result)
    # redeployDb()
