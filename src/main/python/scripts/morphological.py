from re import A
from osgeo import ogr,osr
import platform
import os
import math

# Determine the current operating system
current_os = platform.system()

# Set the appropriate path separator based on the operating system
if current_os == 'Windows':
    separator = '\\'
else:
    separator = '/'

PARENT_DIR = os.getcwd() + '{}src{}main{}python'.format(separator, separator, separator)
OUT_DIR = PARENT_DIR + '{}out{}'.format(separator, separator)

# os.environ['PROJ_LIB'] = r'C:\Users\cieta\AppData\Local\Programs\Python\Python38\Lib\site-packages\osgeo\data\proj'
def segments(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return zip(poly, poly[1:] + [poly[0]])

def perimeter(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return abs(sum(math.hypot(x0-x1,y0-y1) for ((x0, y0), (x1, y1)) in segments(poly)))

def area(shpPath):
    '''计算面积'''
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shpPath, 1)
    layer = dataSource.GetLayer()

    src_srs = layer.GetSpatialRef()  #获取原始坐标系或投影
    tgt_srs = osr.SpatialReference()
    tgt_srs.ImportFromEPSG(32649)  #WGS_1984_UTM_Zone_49N投影的ESPG号，需要改自己的要去网上搜下，这个不难
    transform = osr.CoordinateTransformation(src_srs, tgt_srs) #计算投影转换参数
    # geosr.SetWellKnownGeogCS("WGS_1984_UTM_Zone_49N")

    new_field = ogr.FieldDefn("Area", ogr.OFTReal)  #创建新的字段
    new_field.SetWidth(32)
    new_field.SetPrecision(16)
    layer.CreateField(new_field)
    area = 0
    per = 0
    count = 0
    for feature in layer:
        geom = feature.GetGeometryRef()
        perimeter = feature.GetGeometryRef().Boundary().Length()
        geom2 = geom.Clone()
        geom2.Transform(transform)

        area_in_sq_m = geom2.GetArea()/1000000  #默认为平方米
        # area_in_sq_km = area_in_sq_m / 1000000 #转化为平方公里

        feature.SetField("Area", area_in_sq_m)
        layer.SetFeature(feature)
        area = area + area_in_sq_m
        per = per + perimeter
        count = count + 1

    out = 2*(math.log(per/4))/math.log(A)
    posui = area/count
    print(str(round(area,2)) + ':' + str(round(per,2)) + ":" + str(round(posui,2)) + ":" + str(round(out,2)))


path = OUT_DIR + 't2.shp'
area(path)
