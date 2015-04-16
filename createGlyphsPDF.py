from fontTools.pens.cocoaPen import CocoaPen

# Some configuration
page_format = 'A4' # See http://drawbot.readthedocs.org/content/canvas/pages.html#size for other size-values
my_selection = CurrentFont() # May also be CurrentFont.selection or else

# Init
font = CurrentFont()
size(page_format)
page_width = width()
page_height = height()

# Drawbox Settings
drawbox = {}
drawbox['left_margin'] = 50
drawbox['top_margin'] = 50
drawbox['right_margin'] = 50
drawbox['bottom_margin'] = 200
drawbox['xMin'] = drawbox['left_margin']
drawbox['yMin'] = drawbox['bottom_margin']
drawbox['xMax'] = page_width - drawbox['right_margin']
drawbox['yMax'] = page_width - drawbox['top_margin']
drawbox['width'] = page_width - drawbox['left_margin'] - drawbox['right_margin']
drawbox['height'] = page_height - drawbox['bottom_margin'] - drawbox['top_margin']


print drawbox

def showPageMargins():
    fill(None)
    stroke(0, 0, 1, .1)
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
        stroke(255, 0,0)
        line((drawbox['xMin'], drawbox['yMin'] + self.xHeight_pos*sc), (drawbox['xMin'] + self.glyph.width*sc, drawbox['yMin'] + self.xHeight_pos*sc))
    
    def drawCapHeight(self):
        stroke(255,0,0)
        line((drawbox['xMin'], drawbox['yMin'] + self.capHeight_pos*sc), (drawbox['xMin'] + self.glyph.width*sc, drawbox['yMin'] + self.capHeight_pos*sc))
    
    def drawBaseline(self):
        stroke(255, 0, 0)
        line((drawbox['xMin'], drawbox['yMin'] + abs(descender)*sc), (drawbox['xMin'] + self.glyph.width*sc, drawbox['yMin'] + abs(descender)*sc))
    
    def drawLeftMargin(self):
        stroke(None)
        fill(255,0,0,0.5)
        rect(drawbox['xMin'], drawbox['yMin'], self.glyph.leftMargin*sc, UPM*sc)
    
    def drawRightMargin(self):
        stroke(None)
        fill(255,0,0,0.5)
        rect(drawbox['xMin'] + (self.glyph.width - self.glyph.rightMargin)*sc, drawbox['yMin'], self.glyph.rightMargin*sc, UPM*sc)
        #rect((drawbox['xMax'] - self.glyph.rightMargin)*sc, drawbox['yMin'], self.glyph.width*sc, UPM*sc)
        

                
    def addNewPage(self):
        newPage()
        showPageMargins()
    
    def drawGlyph(self):
        save()
        stroke(None)
        fill(0)
        translate(drawbox['xMin'], 0)
        translate(0, drawbox['yMin'] + abs(descender)*sc)
        scale(sc)        
        
        self._drawGlyph()
        restore()
    
    def center(self, horizontal=True, vertical=True):
        print 'center'
        offset_x = 0
        offset_y = 0
        if horizontal:
            offset_x = (drawbox['width'] - self.glyph.width*sc)/2
        
        if vertical:
            offset_y = (drawbox['height'] - UPM*sc)/2
        
        translate(offset_x, offset_y)
        
        
    
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
        glyph.center()
        glyph.drawLeftMargin()
        glyph.drawRightMargin()
        glyph.drawGlyph()
        glyph.drawBoundingBox()
        
        glyph.drawBaseline()
        glyph.drawXHeight()
        glyph.drawCapHeight()
        
        

