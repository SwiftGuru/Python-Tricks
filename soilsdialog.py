import tkSimpleDialog
import tkFileDialog as tkf
import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = "T:/Soils/SoilApp"
arcpy.env.overwriteOutput = True
gridOptions = options = {}
options['defaultextension']= '.csv'
options['filetypes'] = [('csv files', '.csv'),('exel files','.xls')]
options['initialdir'] = './Grids/'
options['initialfile'] = ''
options['title'] = "Open Grid for the desired field"

inGrid = tkf.askopenfilename(**gridOptions)

outFeature = "points"
coordX = "EASTING"
coordY = "NORTHING"
spRef = r"Coordinate Systems\Projected Coordinate Systems\Utm\Nad 1983\NAD 1983 UTM Zone 11N.prj"
save = "./Temp/points.lyr"
zField = tkSimpleDialog.askstring('Specify Mineral', 'CA,SND,PH')

cellSize = 4
pwer = 2
rstr ="./Temp/idws.tif"
inRaster = "./Temp/outint"
outPolygon = "./Temp/temp.shp"
fieldOptions = options1 = {}
options1['defaultextension']= '.shp'
options1['filetypes'] = [('shape files', '.shp')]
options1['initialdir'] = './Fields'
options1['initialfile'] = ''
options1['title'] = "Open Mask for the desired field"
field = tkf.askopenfilename(**fieldOptions)

dissField = "GRIDCODE"
dissOut = "./Temp/diss.shp"
valField = "Count"
intField = "int"
compField = tkSimpleDialog.askstring('Output mineral','Calcium,Sand,pH')
#resultField = "Sand"
express = "[GRIDCODE]/10"
express2 = "int([Count])"
express3 = "[int]*10"
#express4 = "[SND]"
saveOptions = options2 = {}
options2['defaultextension']= '.shp'
options2['filetypes'] = [('shape files', '.shp')]
options2['initialdir'] = './Results'
options2['initialfile'] = ''
options2['title'] = "Save Result as shape file"
result = tkf.asksaveasfilename(**saveOptions)
#target = r"C:\Users\irudych\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to AGNGIS.sde\GIS.DBO.AGNW2\GIS.DBO.sand_AGNW"


arcpy.MakeXYEventLayer_management(inGrid,coordX,coordY,outFeature,spRef)
print arcpy.GetCount_management(outFeature)
arcpy.SaveToLayerFile_management(outFeature,save)
arcpy.CheckOutExtension("Spatial")
arcpy.env.extent = field
arcpy.env.mask = field
outIDW = Idw(save,zField,cellSize,pwer)
outIDW.save("./Temp/idws.tif")
outInt = Int(rstr)
outInt.save("./Temp/outint")
arcpy.RasterToPolygon_conversion(inRaster,outPolygon,"NO_SIMPLIFY")
arcpy.Dissolve_management(outPolygon,dissOut,dissField)
arcpy.AddField_management(dissOut,valField,"DOUBLE")
arcpy.CalculateField_management(dissOut,valField,express)
arcpy.AddField_management(dissOut,intField,"DOUBLE")
arcpy.CalculateField_management(dissOut,intField, express2)
arcpy.AddField_management(dissOut,compField,"DOUBLE")
arcpy.CalculateField_management(dissOut,compField,express3)
arcpy.DeleteField_management(dissOut,intField)
arcpy.DeleteField_management(dissOut,valField)
arcpy.Dissolve_management(dissOut,result,compField)
#arcpy.Append_management(dissOut,target,"NO_TEST")
