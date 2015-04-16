# Some configuration
page_format = 'A4'
newPage(page_format)


class RegisterGlyph(object):
    
    def __init__(self, glyph):
        self.glyph = glyph
        print 'Registered', self.glyph.name
        self.proportion_ratio = self.getProportionRatio()
    
    def getProportionRatio(self):
        print self.glyph.width
        
        

for g in CurrentFont():
    glyph = RegisterGlyph(g)

