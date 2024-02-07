#!/usr/bin/python3

import json
from osgeo import gdal, gdalconst
import os.path

# https://mrms.nssl.noaa.gov/
# https://vlab.noaa.gov/web/wdtd/mrms-products-guide

def main():
    source_url = ('https://mrms.ncep.noaa.gov' 
        '/data/2D/MergedReflectivityQCComposite/'
        'MRMS_MergedReflectivityQCComposite.latest.grib2.gz')


    ds = gdal.Open(f'/vsigzip//vsicurl/{source_url}')
    gdal.Warp('/vsimem/reprojected.tiff', dstSRS='EPSG:3857', srcDSOrSrcDSTab=ds, resampleAlg=gdalconst.GRA_Average)

    ds = gdal.Open('/vsimem/reprojected.tiff')
    gdal.DEMProcessing('./latest.png', ds, 'color-relief', colorFilename='./radar_ramp.txt', format='png', addAlpha='true')
    
    info = gdal.Info(ds, format='json')
    print(json.dumps(info['wgs84Extent'], indent=2))

    gdal.Unlink('/vsimem/reprojected.tiff')
    ds = None

    if os.path.isfile('./latest.png.aux.xml'):
        os.unlink('./latest.png.aux.xml')

if __name__ == '__main__':
    main()