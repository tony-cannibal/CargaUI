
class Maquina:
    def __init__(self, maquina: list, apps: list = [], grometeras: list = []):
        self.nombre = maquina[0]
        self.area = maquina[1]
        self.subArea = maquina[2]
        self.tipo = maquina[3]
        self.uph = maquina[4]
        self.procesos = maquina[5].split(",")
        self.aplicadores = apps
        self.grometeras = grometeras

    def hasProcesBool(self, proceso):
        if proceso in self.procesos:
            return True
        else:
            return False

    def hasAppBool(self, terminal: str) -> bool:
        if terminal[0:10] in self.aplicadores:
            return True
        else:
            return False

    def hasAppStr(self, terminal: str) -> str:
        if terminal == "":
            return ""
        if terminal[0] != "T":
            return ""
        if terminal[0:10] in self.aplicadores:
            return "ok"
        else:
            return "err"

    def hasGromBool(self, sello: str) -> bool:
        if sello in self.grometeras:
            return True
        else:
            return False

    def hasGromStr(self, terminal: str, sello: str, exeptions: list) -> str:
        if sello in exeptions:
            return ''
        if sello == "" or terminal == "":
            return ""
        if sello[0] != "J":
            return ""
        if sello in self.grometeras:
            return "ok"
        else:
            return "err"

# class Maquina:
#     def __init__(self, maquina: list):
#         self.nombre = maquina[0]
#         self.area = maquina[1]
#         self.tipo = maquina[2]
#         self.uph = maquina[3]
#         self.procesos = maquina[4].split(",")
#
#     def hasProcesBool(self, proceso):
#         if proceso in self.procesos:
#             return True
#         else:
#             return False


# class MaquinaManual(Maquina):
#     def __init__(self, maquina, apps):
#         super().__init__(maquina)
#         self.aplicadores = apps
#
#     def hasAppBool(self, terminal: str) -> bool:
#         if terminal[0:10] in self.aplicadores:
#             return True
#         else:
#             return False
#
#     def hasAppStr(self, terminal: str) -> str:
#         if terminal == "":
#             return ""
#         if terminal[0] != "T":
#             return ""
#         if terminal[0:10] in self.aplicadores:
#             return "ok"
#         else:
#             return "err"
#
#
# class MaquinaAuto(MaquinaManual):
#     def __init__(self, maquina, apps, grometeras):
#         super().__init__(maquina, apps)
#         self.grometeras = grometeras
#
#     def hasGromBool(self, sello: str) -> bool:
#         if sello in self.grometeras:
#             return True
#         else:
#             return False
#
#     def hasGromStr(self, terminal: str, sello: str) -> str:
#         if sello == "" or terminal == "":
#             return ""
#         if sello[0] != "J":
#             return ""
#         if sello in self.grometeras:
#             return "ok"
#         else:
#             return "err"
