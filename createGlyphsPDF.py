# Some configuration
page_format = 'A4' # See http://drawbot.readthedocs.org/content/canvas/pages.html#size for other size-values
my_selection = CurrentFont() # May also be CurrentFont.selection or else


class RegisterGlyph(object):
    
    def __init__(self, glyph):
        self.glyph = glyph
        print 'Registered', self.glyph.name
        self.proportion_ratio = self.getProportionRatio()
    
    def getProportionRatio(self):
        print self.glyph.width
    
    def createPage(self):
        newPage(page_format)
        
        

for g in my_selection:
    glyph = RegisterGlyph(g)
    glyph.createPage()

