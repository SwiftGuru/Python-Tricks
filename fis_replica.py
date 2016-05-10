  #-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      irudych
#
# Created:     26/08/2015
# Copyright:   (c) irudych 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
import arcpy
from arcpy import env

env.workspace = "Database Connections\AGRINW.sde"
env.overwriteOutput = True

inTable = "Database Connections\FIS.sde\FIS.dbo.vm_RM_FieldHistory"
outLocation = "Database Connections\AGRINW.sde"
outTable = "FISData"
inFeatures = "Database Connections\GISReplica.sde\ROWGIS.SDE.AGNW_FIS\ROWGIS.SDE.Fields_All"
outFeatureClass = "FieldData"
delimitedField = arcpy.AddFieldDelimiters(env.workspace, "FieldYear")
expression = delimitedField + " = Year(CURRENT_TIMESTAMP)"
FeatureClass = "Database Connections\AGRINW.sde\FieldData"
Table = "Database Connections\AGRINW.sde\FISData"


sys.argv = [r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py', '-uirudych', '-pwelcome100', '-shttp://agngis2.agreserves.com:6080/arcgis/', '-nAgriNorthwestCrops', '-ostop']
execfile(r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py')

arcpy.Delete_management(FeatureClass)
arcpy.Delete_management(Table)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)

arcpy.TableToTable_conversion(inTable, outLocation, outTable)

sys.argv = [r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py', '-uirudych', '-pwelcome100', '-shttp://agngis2.agreserves.com:6080/arcgis/', '-nAgriNorthwestCrops', '-ostart']
execfile(r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py')

print "This script is awesome!"
