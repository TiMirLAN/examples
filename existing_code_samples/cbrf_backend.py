# 2012
# refactoring required
__author__ = 'timirlan'
from xml.sax import ContentHandler,parse
from datetime import date

USD = 0
EUR = 0
DATESTAMP = date(1990, 12, 31)


class CbrfRatesContentHandler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.founded = []
        self.val = None
        self.should_read_content = False

    def startElement(self, name, attrs):
        if name == 'Valute':
            self.val = []
        if name in ['CharCode', 'Value']:
            self.should_read_content = True
        else:
            self.should_read_content = False

    def characters(self, content):
        if self.should_read_content:
            try:
                self.val.append(float(content.replace(',', '.')))
            except ValueError:
                self.val.append(content)
            finally:
                self.should_read_content = False

    def endElement(self, name):
        if name == 'Valute' and self.val:
            if self.val[0] in ['USD', 'EUR']:
                self.founded.append(self.val)
            self.val = None

    def endDocument(self):
        self.founded = dict(pair for pair in self.founded)


def get_rates():
    handler = CbrfRatesContentHandler()
    parse('http://www.cbr.ru/scripts/XML_daily.asp', handler)
    return handler.founded


def update_rates():
    global USD
    global EUR
    global DATESTAMP
    if date.today() > DATESTAMP:
        data = get_rates()
        USD = "%.2f" % data['USD']
        EUR = "%.2f" % data['EUR']
        DATESTAMP = date.today()
    return USD,EUR,DATESTAMP