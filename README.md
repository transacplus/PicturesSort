# PicturesSort
Recursive Sort of your pictures form iphone based on Exif creation date. 

pip install Pillow

First, copy python script in the root directory you want to sort
In Exif is not found then take the older of creation or modification date
result : 
Sort in directories your files :
AAAA
  - AAAA_MM
      file.jpg ...
...

Programme de TRI des PHOTOS 

Creation de repertoire AAAA_MM en fonction de l'exif ou de la date de creation des fichiers photos 
ou de modification si la date est antérieure à la date de creation 
Deplacaement du fichier en dans le repertoir AAAA_MM
Prerequis : mettre le fichier date.py a la base des images a ranger
Exception : Information et non ecrasement du fichier
Rangement des repertoires AAAA_MM sur dans AAAA

