import os, time, datetime
import shutil
"""
Programme de TRI des PHOTOS 

Creation de repertoire AAAA_MM en fonction de l'exif ou de la date de creation des fichiers photos 
ou de modification si la date est antérieure à la date de creation 
Deplacaement du fichier en dans le repertoir AAAA_MM
Prerequis : mettre le fichier date.py a la base des images a ranger
Exception : Inforamtion et non ecrasement du fichier
Rangement des repertoires AAAA_MM sur dans AAAA

"""
def CountFiles(path,nbfiles):
    """Fonction recurcive pour afficher les fichiers des repertoires"""

    obj = os.scandir(path)

    #print("Files and Directories in '% s':" % path)
    for entry in obj:
        if entry.is_dir():
            nbfiles = CountFiles(path + '\\'+entry.name,nbfiles)
        else :
            #or entry.is_file():
            print(path + '\\'+entry.name)
            nbfiles +=1
            #print (nbfiles)
    return nbfiles

"""
def getFiles(path,r):
    #Fonction recurcive pour afficher les fichiers des repertoires 

    obj = os.scandir(path)

    #print("Files and Directories in '% s':" % path)
    for entry in obj:
        if entry.is_dir():
            r = getFiles(path + '\\'+entry.name,r)
        else :
            #or entry.is_file():
            print(path + '\\'+entry.name)
            r=r+1
            print (r)
    return r

"""

def removeEmptyDir(path):
    #Fonction recurcive pour effacer des repertoires

    obj = os.scandir(path)
    toDelete = True

    for entry in obj:
        #print('rep :' + path + '\\' + entry.name)
        if entry.is_dir():
            if not removeEmptyDir(path + '\\'+entry.name):
                toDelete = False
        else :
            toDelete = False

    if toDelete:
        print('delete  : %s' %  path)
        os.rmdir(path)

    return toDelete

def get_date_creation_or_modification(file) :
    """retourne soit la date de creation
    ou la date de modification en choisissant la plus ancienne """

    """
    print("Modified")
    print(os.stat(file)[-2])
    print(os.stat(file).st_mtime)
    print(os.path.getmtime(file))

    print("Created")
    print(os.stat(file)[-1])
    print(os.stat(file).st_ctime)
    print(os.path.getctime(file))

    print()
    """
    created = os.path.getctime(file)
    #print("Date created: "+time.ctime(created))
    #print("Date created:",datetime.datetime.fromtimestamp(created))
    year1,month1,day1,hour,minute,second=time.localtime(created)[:-3]
    print("Date created: %02d/%02d/%d %02d:%02d:%02d"%(day1,month1,year1,hour,minute,second))
    d1 = datetime.datetime(year1,month1,day1)

    
    modified = os.path.getmtime(file)
    #print("Date modified: "+time.ctime(modified))
    #print("Date modified:",datetime.datetime.fromtimestamp(modified))
    year,month,day,hour,minute,second=time.localtime(modified)[:-3]
    print("Date modified: %02d/%02d/%d %02d:%02d:%02d"%(day,month,year,hour,minute,second))
    d2 = datetime.datetime(year, month,  day)
    if d1 < d2 :
        dir_aaaa_mm = "%02d_%02d" %(year1,month1)
        return str(d1)
    else:
        dir_aaaa_mm = "%02d_%02d" % (year, month)
        return str(d2)
    ###return dir_aaaa_mm

    #print (dir_aaaa_mm)

def get_folder(mydate) :
    """Creer le repertoire AAAA_MM"""

    tmp = list(mydate)
    return ''.join(tmp[0:4]) + '_' + ''.join(tmp[5:7])

def getDateTimeOriginal(file):
    """ Recupere la date de prise de vue de l'image à partir de l'exif """
    # TODO Gerer exception
    from PIL import Image
    from PIL import ExifTags
    from PIL import UnidentifiedImageError
    try :
        exifData = {}
        img = Image.open(file)
        exifDataRaw = img._getexif()
        for tag, value in exifDataRaw.items():
            decodedTag = ExifTags.TAGS.get(tag, tag)
            if decodedTag== 'DateTimeOriginal' :
                return value
            #exifData[decodedTag] = value
        #print (exifData('exifDataRaw'))
    except UnidentifiedImageError as err:
        print('Pas d\'exif dans ce fichier : ' + file)
        return None
    except Exception as err:
        print("getDateTimeOriginal error: {0}".format(err))
        print('Pas d\'exif dans ce fichier : ' + file)
        return None
    return None

def somme (n) :
    if n>1:
        return somme(n-1) + n
    else:
        return 1

def getFiles(path,r):
    """ Fonction recursive pour afficher les fichiers des repertoires """

    obj = os.scandir(path)

    #print("Files and Directories in '% s':" % path)
    for entry in obj:
        if entry.is_dir():
            # Appel recursif
            r = getFiles(path + '\\'+entry.name,r)
        else :
            #or entry.is_file():
            #print(path + '\\'+entry.name)
            """ Traitement du fichier jpg """
            mydate = getDateTimeOriginal(path + '\\'+entry.name)
            if mydate is None:
                print('Erreur date sur fichier ' + entry.name)
                #erreur_fichier += 1
                #i -= 1
                # on recupere la plus ancienne date de creation ou modification fichier
                mydate = get_date_creation_or_modification(path + '\\'+entry.name)

            dir_aaaa_mm = get_folder(mydate)
            # creation du repertoire AAAA_MM
            os.makedirs(dir_aaaa_mm, exist_ok=True)
            try:
                shutil.move(path + '\\'+entry.name, dir_aaaa_mm)
                listRepaaaamm.append(dir_aaaa_mm)
            except  shutil.Error as err:
                print("Shutil error: {0}".format(err))
            r=r+1

    return r

def moveAAAA_MM2AAAA(listRep):
    """ Deplace le repertoire 2019_02 dans le repertoire 2019 """

    for rep in set(listRep):
        strRep=list(rep)
        aaaa=strRep[0:4]
        # creation du repertoire AAAA_MM
        aaaa=''.join(aaaa)
        os.makedirs(aaaa, exist_ok=True)

        try:
            shutil.move(rep, aaaa)
            print('Déplacement du répertoire ' + rep +' dans '+ aaaa)
        except  shutil.Error as err:
            print("Shutil error: {0}".format(err))
    pass

if __name__ == "__main__":

    nbfiles=0
    listRepaaaamm = []
    path=os.getcwd()

    TotalFichiers = CountFiles(path,nbfiles)

    # recursion
    fichierDeplaces = getFiles(path,0)
    moveAAAA_MM2AAAA(listRepaaaamm)
    removeEmptyDir(path)
    print('Nombre de fichiers déplacés :' + str(fichierDeplaces))
    print('Nombre Total de fichiers :' + str(TotalFichiers))
