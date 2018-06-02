from PIL import Image
import datetime
import piexif
import os
import shutil

#Needed to identify image as JPEG instead of MPO
from PIL import JpegImagePlugin
JpegImagePlugin._getmp = lambda x: None

def imgDateAdjust(img, hoursDelta):
    exifDict = piexif.load(img.info['exif'])
    imgOriDateStr=exifDict["Exif"][36867].decode("utf-8")
    imgOriDateDateTime = datetime.datetime.strptime(imgOriDateStr,'%Y:%m:%d %H:%M:%S')

    print("original image date:"+imgOriDateStr)

    imgModDateDateTime=imgOriDateDateTime-datetime.timedelta(hours=-hoursDelta)
    imgModDateStr=imgModDateDateTime.strftime('%Y:%m:%d %H:%M:%S')
    exifDict["Exif"][36867]=imgModDateStr

    print("Updated image date:"+imgModDateStr)

    exifBytes=piexif.dump(exifDict)
    piexif.insert(exifBytes, img.filename)
    modifiedImg = Image.open(img.filename)

    return(modifiedImg)

def batchProcessing(folderPath):
    print("*******************Start Batch Processing*******************")
    imgExtensions = ("jpg","jpeg","JPG","JPEG")
    fileNames = [fn for fn in os.listdir(folderPath)
                        if fn.endswith(imgExtensions)]

    NewImgDirectory="/Modified Images"
    cwd = os.getcwd()
    if not os.path.exists(cwd+NewImgDirectory):
        os.makedirs(cwd+NewImgDirectory)

    for item in fileNames:
        print("Processing: "+item)
        shutil.copyfile(folderPath+"/"+item, cwd+NewImgDirectory+"/"+item)
        img=Image.open(cwd+NewImgDirectory+'/'+item)
        imgDateAdjust(img, -12)
        print("end processing: "+item)
        print("")
    print("********************End Batch Processing********************")

def main():
    batchProcessing("C:\DATA\Professionnel\Programmation\PictureEditorLib\Original Images")
    return()

main()
