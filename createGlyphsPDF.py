from fontTools.pens.cocoaPen import CocoaPen

# Some configuration
page_format = 'A4' # See http://drawbot.readthedocs.org/content/canvas/pages.html#size for other size-values
margins = (0,0,0,0) # left, top, right, bottom
my_selection = CurrentFont() # May also be CurrentFont.selection or else

# Init
font = CurrentFont()
size(page_format)
page_width = width()
page_height = height()
drawbox = {
    'xMin': margins[0],
    'yMin': margins[3],
    'xMax': page_width - margins[2],
    'yMax': page_width - margins[1],
    'width': page_width - margins[0] - margins[2],
    'height': page_height - margins[1] - margins[3]
    }

print drawbox

def showPageMargins():
    fill(None)
    stroke(1, 0, 0, .3)
    rect(drawbox['xMin'], drawbox['yMin'], drawbox['width'], drawbox['height'])



class RegisterGlyph(object):
    
    def __init__(self, glyph):
        self.glyph = glyph
        #print 'Registered glyph:', self.glyph.name
        
        self.getGlyphSizeData()
    
    def getGlyphSizeData(self):
        self.xMin, self.yMin, self.xMax, self.yMax = self.glyph.box
        self.w = self.xMax - self.xMin 
        self.h = self.yMax - self.yMin
        self.xHeight_pos = xHeight + abs(descender)
        self.capHeight_pos = capHeight + abs(descender)
        self.x_pos = self.glyph.leftMargin + drawbox['xMin']
        print self.x_pos
        
        #print self.xMin, self.yMin, self.xMax, self.yMax
    
    def getScale(self):
        if self.w > self.h:
            return drawbox['width']/self.w
        else:
            return 1
            #return drawbox['height']/self.h
    
    def drawBoundingBox(self):
        stroke(255,0,0)
        fill(None)
        rect(drawbox['xMin'], drawbox['yMin'], self.glyph.width*sc, UPM*sc)
    
    def drawXHeight(self):
        stroke(255,0,0)
        line((drawbox['yMin'], self.xHeight_pos*sc), (self.glyph.width*sc, self.xHeight_pos*sc))
    
    def drawCapHeight(self):
        stroke(255,0,0)
        line((drawbox['yMin'], self.capHeight_pos*sc), (self.glyph.width*sc, self.capHeight_pos*sc))
    
    def drawBaseline(self):
        stroke(255, 0, 0)
        line((drawbox['yMin'], abs(descender)*sc), (self.glyph.width*sc, abs(descender)*sc))
    
    def drawLeftMargin(self):
        stroke(None)
        fill(255,0,0,0.5)
        rect(drawbox['xMin'], drawbox['yMin'], self.glyph.leftMargin*sc, UPM*sc)
    
    def drawRightMargin(self):
        stroke(None)
        fill(255,0,0,0.5)
        rect((self.glyph.width - self.glyph.rightMargin)*sc, drawbox['yMin'], self.glyph.rightMargin*sc, UPM*sc)
        #rect((drawbox['xMax'] - self.glyph.rightMargin)*sc, drawbox['yMin'], self.glyph.width*sc, UPM*sc)
        

                
    def addNewPage(self):
        newPage()
        showPageMargins()
    
    def drawGlyph(self):
        save()
        stroke(None)
        fill(0)
        scale(sc)
        # Move to box
        # Keep in mind that you don’t have to use sc here, since everything is scaled now
        # TO DO: I may use the scale globally in this class?!
        translate(0, abs(descender))
        
        self._drawGlyph()
        restore()
        
        
    
    def _drawGlyph(self):
        pen = CocoaPen(self.glyph.getParent())
        self.glyph.draw(pen)
        drawPath(pen.path)



def getMaxWidth():
    max_width = 0
    for g in my_selection:
        if g.width > max_width:
            max_width = g.width

    return max_width

def getScale():
    # The glyphs should be displayed as big as possible.
    # So the most wide glyph will be the base for the scaling.
    
    sc = drawbox['width']/max_width
    return sc

    
        
max_width = getMaxWidth()
sc = getScale()
UPM = font.info.unitsPerEm
xHeight = font.info.xHeight
capHeight = font.info.capHeight
ascender = font.info.ascender
descender = font.info.descender

for g in my_selection: 
    if len(g) > 0: # Ignore whitespace glyphs
        glyph = RegisterGlyph(g)
        glyph.addNewPage()
        glyph.drawLeftMargin()
        glyph.drawRightMargin()
        glyph.drawGlyph()
        glyph.drawBoundingBox()
        
        glyph.drawBaseline()
        glyph.drawXHeight()
        glyph.drawCapHeight()
        
        

