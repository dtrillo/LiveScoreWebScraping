
import unicodedata  # Tildes http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado/

nl = "\n"
# Elimina TILDES
def elimina_tildes(s, optional=True):
    tmp = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    if optional:
        tmp = tmp.replace('*', '').replace("'", "").replace('"', '').strip()
    return tmp


class PartidosWeb:
    estado = {0: 'No iniciado', 1: 'En juego', 2: 'Finalizado'}
    """ Partidos recuperados de BetFair """
    def __init__(self, equipolocal, equipovisitante, res, minuto=0, fecha=None, debug=False):
        # Cuotas y conversión a Porcentajes usando la clase "cuotas2porc"
        # PartidoBasico.__init__(self)
        self.eq_local, self.eq_vis = '', ''
        self.debug = debug
        self.eq_local = elimina_tildes(equipolocal.strip())
        self.eq_vis = elimina_tildes(equipovisitante.strip())
        self.res = res.replace("?", "").strip()      # Elimino los marcadores ? - ?
        self.goll, self.golv = 0, 0
        self.minuto = minuto.strip()
        self._estado()
        if self.minuto == 0:
            self.res = ''
        self.fecha = fecha  # Fecha en que se juega el partido

        if res:
            tmp = self.res.split("-")
            try:
                self.goll, self.golv = int(tmp[0].strip()), int(tmp[1].strip())
            except:
                self.goll, self.golv = 0, 0

    def _estado(self):
        if self.minuto == 'FT':
            self.idestado = 2
        elif ":" in self.minuto:
            self.idestado = 0
        else:
            self.idestado = 1 # En juego

    def valor_1x2(self):
        if self.res:
            if self.goll == self.golv:
                return 'X'
            else:
                valor = "2" if self.golv > self.goll else "1"
                return valor
        else:
            return ''

    def dato(self):
        return {"idpartido": self._idpartido, "goll": self.goll,
                "golv": self.golv, "dgol": self.goll - self.golv,
                "minuto": self.minuto, "signo": self.valor_1x2(),
                "actualizado": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    def __str__(self):
        tmp = self.eq_local + " - " + self.eq_vis
        if len(self.res)>0:
            tmp += " ==> ( " + str(self.goll) + " - " + str(self.golv) + " ) --> " + self.valor_1x2()
        else:
            if self.res:
                tmp += str(self.goll) + " - " + str(self.golv)
        return tmp + " - %s" % self.estado[self.idestado]

