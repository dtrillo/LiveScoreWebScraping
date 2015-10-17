import requests

class Downloading:
    """ Clase para recuperar código HTML de una URL """
    def necesita_proxy(self):
        url = "http://www.bing.es"
        html = self._get_url(url)
        if len(html) == 0 and len(self.proxy) > 0:
            self.sesion.proxies = {"http": self.proxy, "https": self.proxy}
            html = self._get_url(url)
            if len(html) == 0:
                self.sesion.proxies = {}
                self.wInternet = False

    def _get_url(self, url):
        if self.wInternet == False: return ''
        try:
            r = self.sesion.get(url, timeout=self.timeout)
            return r.text
        except:
            return ''

    def __init__(self, proxy = '', t_timeout = 15, timesleep = 2, debug = False):
        self.sesion = requests.Session()
        self.proxy = proxy
        self.wInternet = True
        self.timeout = t_timeout
        self.necesita_proxy()
        self.debug = debug
        if debug: print("Downloading ... creado!")
        self.__timesleep = timesleep  # Pendiente de ELIMINAR

    def gethtml(self, url, fichHTML='', onlydownload=False):
        """ Recupera HTML de url y lo guarda en fichHTML - Llama a gethtml2 """
        if onlydownload: fichHTML = ''
        texto = self._get_url(url)
        tmp = "    Recibido: %s" % url
        #try:
        if texto and fichHTML:
                save_file(fichHTML, texto) # Grabo fichero
                tmp += nl + "    Guardando en ... %s" % fichHTML
        #except Exception as ex:
        #    _, _, ex_traceback = sys.exc_info()
            # log_traceback(ex, ex_traceback)

        if self.debug:
            print (tmp)
        return texto, not self.wInternet

    def gethtml2(self, url, fichHTML='', onlydownload=False):
        """ Devuelve el HTML, y en caso de error, devuelve '' """
        texto, lee = self.gethtml(url, fichHTML, onlydownload)
        return texto
