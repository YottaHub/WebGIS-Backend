import random
import sys
from osgeo import gdal,ogr,osr
import numpy as np
import os
import shutil
import platform

# Determine the current operating system
current_os = platform.system()

# Set the appropriate path separator based on the operating system
if current_os == 'Windows':
    separator = '\\'
else:
    separator = '/'

PARENT_DIR = os.getcwd() + '{}src{}main{}python'.format(separator, separator, separator)
OUT_DIR = PARENT_DIR + '{}out{}'.format(separator, separator)
NIGHT_LIGHT_DIR = PARENT_DIR + '{}rasters{}NightLight{}'.format(separator, separator, separator)
#os.environ['PROJ_LIB'] = r'C:\Users\cieta\AppData\Local\Programs\Python\Python38\Lib\site-packages\osgeo\data\proj'


def raster2vector(raster_path, vecter_path, field_name="class", ignore_values = None):

    # 读取路径中的栅格数据
    raster = gdal.Open(raster_path)
    # in_band 为想要转为矢量的波段,一般需要进行转矢量的栅格都是单波段分类结果
    # 若栅格为多波段,需要提前转换为单波段
    band = raster.GetRasterBand(1)

    # 读取栅格的投影信息,为后面生成的矢量赋予相同的投影信息
    prj = osr.SpatialReference()
    prj.ImportFromWkt(raster.GetProjection())


    drv = ogr.GetDriverByName("ESRI Shapefile")
    # 若文件已经存在,删除
    if os.path.exists(vecter_path):
        drv.DeleteDataSource(vecter_path)

    # 创建目标文件
    polygon = drv.CreateDataSource(vecter_path)
    # 创建面图层
    poly_layer = polygon.CreateLayer(vecter_path[:-4], srs=prj, geom_type=ogr.wkbMultiPolygon)
    # 添加浮点型字段,用来存储栅格的像素值
    field = ogr.FieldDefn(field_name, ogr.OFTReal)
    poly_layer.CreateField(field)

    # FPolygonize将每个像元转成一个矩形，然后将相似的像元进行合并
    # 设置矢量图层中保存像元值的字段序号为0
    gdal.Polygonize(band, band, poly_layer, 0)

    # 删除ignore_value链表中的类别要素
    if ignore_values is not None:
        for feature in poly_layer:
            class_value = feature.GetField('class')
            for ignore_value in ignore_values:
                if class_value==ignore_value:
                    # 通过FID删除要素
                    poly_layer.DeleteFeature(feature.GetFID())
                    break

    polygon.SyncToDisk()
    polygon = None

    uni(OUT_DIR + 't1.shp',OUT_DIR + 't2.shp')

def uni(shpPath, fname):
    """
    :param shpPath: 输入的矢量路径
    :param fname: 输出的矢量路径
    :return: 
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shpPath, 1)
    layer = dataSource.GetLayer()

    # 新建DataSource，Layer
    out_ds = driver.CreateDataSource(fname)
    out_lyr = out_ds.CreateLayer(fname, layer.GetSpatialRef(), ogr.wkbPolygon)
    def_feature = out_lyr.GetLayerDefn()
    # 遍历原始的Shapefile文件给每个Geometry做Buffer操作
    # current_union = layer[0].Clone()
    # print('the length of layer:', len(layer))
    if len(layer) == 0:
        return

    for i, feature in enumerate(layer):
        geometry = feature.GetGeometryRef()
        if i == 0:
            current_union = geometry.Clone()
        current_union = current_union.Union(geometry).Clone()

        if i == len(layer) - 1:
            out_feature = ogr.Feature(def_feature)
            out_feature.SetGeometry(current_union)
            out_lyr.ResetReading()
            out_lyr.CreateFeature(out_feature)



def ChangeToJson():
    # print("Starting........")
    vector = OUT_DIR + "t2.shp"
    output = OUT_DIR + 't2.json'
    #打开矢量图层
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    shp_ds = ogr.Open(vector)
    # print("sadasd",shp_ds)
    shp_lyr = shp_ds.GetLayer(0)

    # 创建结果Geojson
    baseName = os.path.basename(output)
    out_driver = ogr.GetDriverByName('GeoJSON')
    out_ds = out_driver.CreateDataSource(output)
    if out_ds.GetLayer(baseName):
        out_ds.DeleteLayer(baseName)
    out_lyr = out_ds.CreateLayer(baseName, shp_lyr.GetSpatialRef())
    out_lyr.CreateFields(shp_lyr.schema)
    out_feat = ogr.Feature(out_lyr.GetLayerDefn())

    #生成结果文件
    for feature in shp_lyr:
        out_feat.SetGeometry(feature.geometry())
        for j in range(feature.GetFieldCount()):
            out_feat.SetField(j, feature.GetField(j))
        out_lyr.CreateFeature(out_feat)

    del out_ds
    del shp_ds
    # print("Success........")


def setDir(filepath):
    '''
    param filepath:需要创建的文件夹路径
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

def direct(a,b,c):
    setDir(OUT_DIR)
    files = os.listdir(NIGHT_LIGHT_DIR)  # 得到文件夹下的所有文件名称
    in_tif = NIGHT_LIGHT_DIR + separator + files[a]  # 构造绝对路径
    if b == 1:
        in_shp = PARENT_DIR + '{}features{}长江三角洲{}长江三角洲.shp'.format(separator, separator, separator)
    elif b == 2:
        in_shp = PARENT_DIR + '{}features{}珠江三角洲{}珠江三角洲.shp'.format(separator, separator, separator)
    elif b == 3:
        in_shp = PARENT_DIR + '{}features{}京津冀{}京津冀城市群.shp'.format(separator, separator, separator)
    elif b == 4:
        in_shp = PARENT_DIR + '{}features{}长江中下游{}长江中下游.shp'.format(separator, separator, separator)
    elif b == 5:
        in_shp = PARENT_DIR + '{}features{}成渝城市群{}成渝.shp'.format(separator, separator, separator)
    # print(in_tif)
    zoneStatic(in_tif,in_shp,c)
    # print(a+b)
    return a+b

def zoneStatic(input_tif,input_shp,c):
    input_raster=gdal.Open(input_tif)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(input_shp,1)  #第二个参数为0是只读，为1是可写
    if dataSource is None:#判断是否成功打开
        print('could not open')
        sys.exit(1)


    # feat = layer.GetFeature(i)		 #提取数据层中的第一个要素
    # featureName = feat.GetField('NAME')   #读取该要素字段名为'FieldID'的值，注意读取'shape'字段会报错
    output_file = OUT_DIR + str(random.randint(100000,999999)) + 'zone'  + '.tif'
    # 开始裁剪
    gdal.SetConfigOption("GDALWARP_IGNORE_BAD_CUTLINE", "YES")
    ds = gdal.Warp(output_file,
                   input_raster,
                   format = 'GTiff',
                   cutlineDSName = input_shp,
                   # cutlineWhere="NAME = " +"'" + featureName + "'",
                   cropToCutline=True,
                   dstNodata = -9999)
    statisRaster = gdal.Open(output_file)
    cols = statisRaster.RasterXSize
    rows = statisRaster.RasterYSize
    band = statisRaster.GetRasterBand(1)
    geoTransform = statisRaster.GetGeoTransform()  # 是一个list,存储着栅格数据集的地理坐标信息
    projection = statisRaster.GetProjection()
    nodata = band.GetNoDataValue()
    data = statisRaster.ReadAsArray(0,0,cols,rows).astype(np)
    # data2 = np.ma.masked_equal(data,60)


    # value = 63
    # sum = 0
    # while value > 0 : 
    #     n = np.sum(data == 60)
    #     sum = sum + n
    #     value = value - 1
    #     if sum > c :
    #         break
    for i in range(0,rows):
        for j in range(0,cols):
            if data[i][j] != nodata:
                if data[i][j] < c:
                    data[i][j] =-99
            else:
                data[i][j] = -99

    mask = np.less(data,c)   #设置掩膜
    resultPath = OUT_DIR + 't1.tif'
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    ds = driver.Create(resultPath, cols, rows, 1, gdal.GDT_Float32)
    ds.SetGeoTransform(geoTransform)
    ds.SetProjection(projection)
    ds.GetRasterBand(1).SetNoDataValue(-99)
    ds.GetRasterBand(1).WriteArray(data)
    ds = None

    resultPath = OUT_DIR + 't2.tif'
    output_format = "GTiff"
    driver = gdal.GetDriverByName(output_format)
    ds = driver.Create(resultPath, cols, rows, 1, gdal.GDT_Float32)
    ds.SetGeoTransform(geoTransform)
    ds.SetProjection(projection)
    ds.GetRasterBand(1).SetNoDataValue(-99)
    ds.GetRasterBand(1).WriteArray(mask)
    ds = None
    raster2vector(OUT_DIR + 't1.tif', OUT_DIR + 't1.shp','class',[-99])

    # mask = np.greater(data,10)   #设置掩膜

    # print(featureName + ":" + str(50))

def clip(input_tif,input_shp):

    # tif输入路径，打开文件

    # 矢量文件路径，打开矢量文件
    input_raster=gdal.Open(input_tif)
    output_file = OUT_DIR + str(random.randint(100000,999999))  + '.tif'
    # 开始裁剪
    ds = gdal.Warp(output_file,
                   input_raster,
                   format = 'GTiff',
                   cutlineDSName = input_shp,
                   cropToCutline=True,
                   dstNodata = -9999)

if __name__ == '__main__':
    dict=[]
    for i in range(1, len(sys.argv)):
        url = int(sys.argv[i])
        dict.append(url)
    # direct(3,3,50)
    direct(dict[1],dict[0],dict[2])
    ChangeToJson()
with open(OUT_DIR + 't2.json') as txtfile2:
    print(txtfile2.read())
