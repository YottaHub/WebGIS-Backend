import random
import sys
from osgeo import gdal,ogr
import numpy as np
import os
import platform
import shutil

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

# os.environ['PROJ_LIB'] = r'C:\Users\cieta\AppData\Local\Programs\Python\Python38\Lib\site-packages\osgeo\data\proj'

def setDir(filepath):
    '''
    param filepath:需要创建的文件夹路径
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

def add(a,b):
    setDir(OUT_DIR)
    files = os.listdir(NIGHT_LIGHT_DIR)  # 得到文件夹下的所有文件名称
    in_tif = NIGHT_LIGHT_DIR + files[a]  # 构造绝对路径
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
    zoneStatic(in_tif,in_shp)
    return a+b

def zoneStatic(input_tif,input_shp):
    input_raster=gdal.Open(input_tif)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(input_shp,1)  #第二个参数为0是只读，为1是可写
    if dataSource is None:#判断是否成功打开d
        print('could not open')
        sys.exit(1)
    layer = dataSource.GetLayer(0)   #读取第一个图层
    n = layer.GetFeatureCount()
    # print('Feature count:',n)
    for i in range(n):
        feat = layer.GetFeature(i)		 #提取数据层中的第一个要素
        featureName = feat.GetField('NAME')   #读取该要素字段名为'FieldID'的值，注意读取'shape'字段会报错
        output_file = OUT_DIR + str(random.randint(100000,999999)) + 'zone'  + '.tif'
        # 开始裁剪
        gdal.SetConfigOption("GDALWARP_IGNORE_BAD_CUTLINE", "YES")
        #print(output_file, input_raster)
        ds = gdal.Warp(output_file,
                       input_raster,
                       format = 'GTiff',
                       cutlineDSName = input_shp,
                       cutlineWhere="NAME = " +"'" + featureName + "'",
                       cropToCutline=True,
                       dstNodata = -9999)
        statisRaster = gdal.Open(output_file)
        cols = statisRaster.RasterXSize
        rows = statisRaster.RasterYSize
        band = statisRaster.GetRasterBand(1)
        data = statisRaster.ReadAsArray(0,0,cols,rows).astype(np)
        mask = np.greater(data,10)   #设置掩膜
        data2 = np.ma.masked_equal(data,0)
        data3 = np.ma.masked_equal(data2,1)
        data4 = np.ma.masked_equal(data3,2)
        data5 = np.ma.masked_equal(data4,3)
        data6 = np.ma.masked_equal(data5,4)
        data7 = np.ma.masked_equal(data6,5)
        data8 = np.ma.masked_equal(data7,6)
        data9 = np.ma.masked_equal(data8,7)
        data10 = np.ma.masked_equal(data9,8)
        data11 = np.ma.masked_equal(data10,9)
        data12 = np.ma.masked_equal(data11,10)
        count = np.sum(mask)
        #读取掩膜区域栅格
        average = np.around(np.sum(data12)/count,2)
        print(featureName + ":" + str(average))



def clip(input_tif,input_shp):

    # tif输入路径，打开文件

    # 矢量文件路径，打开矢量文件
    input_raster=gdal.Open(input_tif)
    output_file = OUT_DIR + separator + input_tif.split('.')[0].split('\\')[-1] + str(random.randint(100000,999999))  + '.tif'
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
    add(1, 3)
