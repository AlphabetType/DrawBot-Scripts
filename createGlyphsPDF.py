from fontTools.pens.cocoaPen import CocoaPen

# Some configuration
page_format = 'A4' # See http://drawbot.readthedocs.org/content/canvas/pages.html#size for other size-values
margins = (50,50,50,50) # left, top, right, bottom
my_selection = CurrentFont() # May also be CurrentFont.selection or else

# Init
size(page_format)
page_width = width()
page_height = height()
drawbox = {
    'xMin': margins[0],
    'yMin': margins[3],
    'width': page_width - margins[0] - margins[2],
    'height': page_height - margins[1] - margins[3]
    }




class RegisterGlyph(object):
    
    def __init__(self, glyph):
        self.glyph = glyph
        #print 'Registered glyph:', self.glyph.name
        
        self.proportion_ratio = self.getProportionRatio()
    
    def getProportionRatio(self):
        xMin, yMin, xMax, yMax = self.glyph.box
        self.w = xMax - xMin 
        self.h = yMax - yMin
        ratio = self.w/self.h
        
        return ratio
        
    def drawGlyphOnNewPage(self):
        newPage()
        print 
        self._drawGlyph()
    
    def _drawGlyph(self):
        pen = CocoaPen(self.glyph.getParent())
        self.glyph.draw(pen)
        drawPath(pen.path)
        
        

for g in my_selection: 
    if len(g) > 0: # Ignore whitespace glyphs
        glyph = RegisterGlyph(g)
        glyph.drawGlyphOnNewPage()

