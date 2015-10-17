# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
__author__ = 'dtrillo'

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

    def esta_equipo(self, equipo):
        return equipo.upper() == self.eq_local.upper() or equipo.upper() == self.eq_vis.upper()

    def __str__(self):
        tmp = "%s %s - %s %s" % (self.eq_local, self.goll, self.golv, self.eq_vis)
        t_estado = self.minuto if self.idestado == 1 else self.estado[self.idestado]
        if self.estado > 0:
            t_estado += " ==> (%s) " % (self.valor_1x2())
        return tmp + " - %s" % t_estado

