  #-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      swiftguru
#
# Created:     26/08/2015
# Copyright:   (c) swiftguru 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
import arcpy
from arcpy import env
#house keeping
env.workspace = "Database Connections\Production.sde"
env.overwriteOutput = True #you really dont need this since you are not editing anything

#variables

#these variables are for TableToTable_conversion
inTable = "Database Connections\SQL.sde\SQL.dbo.Table"
outLocation = "Database Connections\Production.sde"
outTable = "Table"

#these variables are for FeatureClassToFeatureClass_conversion
inFeatures = "Database Connections\GIS.sde\GIS.SDE.Features"
outFeatureClass = "Features"

# additional SQL querry on the feature class, selecting current year.
delimitedField = arcpy.AddFieldDelimiters(env.workspace, "Year")
expression = delimitedField + " = Year(CURRENT_TIMESTAMP)"

#these variables are for deletion of existing datasets
existingFeatures = "Database Connections\Production.sde\Features"
existingTable = "Database Connections\Production.sde\Table"


# stoping ArchGIS service to remove schema lock.
sys.argv = [r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py', '-uuser', '-ppassword', '-shttp://gisserver.yourdomain.com:6080/arcgis/', '-nGISService', '-ostop']
execfile(r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py')

# deleting existing datasets
arcpy.Delete_management(existingFeatures)
arcpy.Delete_management(existingTable)

#copying new updated features from GIS and SQL servers
arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)

arcpy.TableToTable_conversion(inTable, outLocation, outTable)

# starting ArchGIS service to renew schema lock.
sys.argv = [r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py', '-uuser', '-ppassword', '-shttp://gisserver.yourdomain.com:6080/arcgis/', '-nGISService', '-ostart']
execfile(r'C:\Program Files\ArcGIS\Server\tools\admin\manageservice.py')

#just for fun
print "This script is awesome!"
