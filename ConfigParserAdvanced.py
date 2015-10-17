# coding: utf-8

""" ConfigParserAdvanced,
developer by David Trillo Montero
write me at manejandodatos@gmail.com

Visit my website: http://www.manejandodatos.es
# Version 0.8.0 - 20150120
    Mejora de escritura PEP 8
# Version 0.8.0 - 20140704
	self.get() modificado para que se ajuste al tipo de dato
# Version 0.7.0 - 20140110
"""

import ConfigParser

class ConfigParserAdvanced():
    def __init__(self, sfile, main_section='', getdefault=''):
        self.file = sfile
        self.reload()
        self.main_section = self.config.sections()[0] if len(self.config.sections()) == 1 else main_section
        self.getdefault = getdefault

    def reload(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.file)

    def defaultValue(self, value):
        self.getdefault = value

    def read(self, sfilename):
        return self.config.read(sfilename)

    def sections(self):
        """ Sections of the Config File """
        return self.config.sections()

    def main_section(self, new_section):
        """ Change Section """
        self.main_section = new_section

    def options(self, new_section):
        """ Options from a NEW SECTION, that become Main_Section """
        self.main_section = new_section
        return self.config.options(self.main_section) if self.main_section else []

    def add_section(self, new_section):
        """ Add a New section """
        self.main_section = new_section
        self.config.add_section(self.main_section)

    # GET functions
    def get(self, section, option, defval=None):
        """ Get a VALUE of an option, of the SECTION"""
        self.main_section = section
        try:
            return self.ajustavalor(self.config.get(self.main_section, option))
        except:
            return defval if defval else self.getdefault

    @staticmethod
    def ajustavalor(valor):
        verdadero = ["Verdadero", "verdadero", "true", "True"]
        falso = ["Falso", "False", "falso", "false"]
        valor2 = valor
        if valor in verdadero:
            valor2 = True
        elif valor == falso:
            valor2 = False
        else:
            try:
                valor2 = float(valor)
            except:
                valor2 = valor
        return valor2

    def getboolean(self, section, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        self.main_section = section
        try:
            return self.config.getboolean(self.main_section, option)
        except:
            return False
    def getfloat(self, section, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        self.main_section = section
        try:
            return self.config.getfloat(self.main_section, option)
        except:
            return False

    def getint(self, section, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        self.main_section = section
        try:
            return self.config.getint(self.main_section, option)
        except:
            return False
    def has_option(self, section,option):
        """ Exists OPTION in SECTION """
        self.main_section = section
        try:
            return self.config.has_option(self.main_section, option)
        except:
            return False

    # get FROM the Main_SECTION
    def options2(self):
        """ Options from Main_Section """
        return self.options(self.main_section)

    def get2(self, option):
        """ Get a VALUE of an option, of the MAIN_SECTION"""
        return self.get(self, self.main_section, option)

    def getboolean2(self, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        return self.getboolean(self.main_section, option)

    def getint2(self, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        return self.getint(self.main_section, option)

    def getfloat2(self, option):
        """ GET a BOOLEAN Value of an OPTION of the SECTION """
        return self.getfloat(self.main_section, option)

    def has_option2(self, option):
        """ Exists OPTION in MAIN_SECTION """
        return self.has_option(self.main_section, option)

    def has_section(self, section):
        try:
            return self.config.has_section(section)
        except:
            return False

    # Write Data to self.File
    def writedata(self):
        sf = open(self.file,"w")  # Necesito el fichero INI "preparado" para grabar informacion
        self.config.write(sf)
        sf.close()

    def set(self, section, option, value = None, save=True):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.main_section = section
        self.config.set(self.main_section, option, str(value))
        if save:
            self.writedata()

    # Write OPTION-VALUE to MAIN_SECTION
    def set2(self, option, value=None, save=True):
        """ Set data on the MAIN_SECTION  """
        self.set(self.main_section, option, value, save)

# def optionxform(self, optionstr):
# return self.config.optionxform(optionstr)
# def readfp(self, fp):
# return self.config.readfp(fp)
# def items(self, section):
# return self.config.items(self.main_section)
