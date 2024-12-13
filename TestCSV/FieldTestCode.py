from qgis.PyQt import QtGui

fn = "C:/Nay/SolarCells_Project/Data/TestData/Pl1_20231210_Gov_buildings_LOD2_att.shp"

layer = QgsVectorLayer(fn, '','ogr')

# for field in layer .fields():
#     print(field.name())
    
# Graduaed Symbology
tf = 'rooftop'
rangeList = []
opacity = 1

# Create Symbology for First Range
minVal = 0.0
maxVal = 10.5

lab = 'Group 1'

color1 = QtGui.QColor('#ffee00')

symbol = QgsSymbol.defaultSymbol(layer.geometryType())
symbol.setColor(color1)
symbol.setOpacity(opacity)

range1 = QgsRendererRange(minVal, maxVal, symbol, lab)
rangeList.append(range1)

# Create Symbology for Second Range
minVal = 10.5
maxVal = 20.5

lab = 'Group 2'

color2 = QtGui.QColor('#00eeff')

symbol = QgsSymbol.defaultSymbol(layer.geometryType())
symbol.setColor(color2)
symbol.setOpacity(opacity)

range2 = QgsRendererRange(minVal, maxVal, symbol, lab)
rangeList.append(range2)

# Apply Range ot layer
groupRenderer = QgsGraduatedSymbolRenderer('', rangeList)
groupRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)

groupRenderer.setClassAttribute(tf)

layer.setRenderer(groupRenderer)

QgsProject.instance().addMapLayer(layer)

