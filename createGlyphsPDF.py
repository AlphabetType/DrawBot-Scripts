# Some configuration
page_format = 'A4' # See http://drawbot.readthedocs.org/content/canvas/pages.html#size for other size-values
my_selection = CurrentFont() # May also be CurrentFont.selection or else


class RegisterGlyph(object):
    
    def __init__(self, glyph):
        self.glyph = glyph
        print 'Registered glyph:', self.glyph.name
        
        self.proportion_ratio = self.getProportionRatio()
    
    def getProportionRatio(self):
        xMin, yMin, xMax, yMax = self.glyph.box
        self.w = xMax - xMin 
        self.h = yMax - yMin
        ratio = self.w/self.h
        
        return ratio
        
    def drawGlyphOnNewPage(self):
        newPage(page_format)
    
    def _drawGlyph(self):
        pen = CocoaPen(self.glyph.getParent())
        self.glyph.draw(pen)
        drawPath(pen.path)
        
        

for g in my_selection:
    glyph = RegisterGlyph(g)
    glyph.drawGlyphOnNewPage()

