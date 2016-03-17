# RecipPicks_2DLine

Script designed to get reciprocal picks from seismic data in a 2D line geometry. Script as currently designed requires that shots be named numerically in order of smaller to larger offset, so a shot with a lower number (e.g. shot 1) will have a smaller absolute offset (along the 2D line) than a shot with a larger number (e.g. shot 2).

Files with picks can have many rows/columns, but each row should be a different pick and, with column 1 = source-receiver offset in m, and column 2 = unreduced travel time in seconds. No headers. 

Pick files need to be named consistently, with naming convention specified in the RecipPicks_ConfigFile.txt (sample included in repository). For the sample provided, a file of picks from shot 05 with arrival type 2 (would refer to, for example, picks of PmP mantle reflections):

[fname_prearrival][arrivaltype][fname_preshot][shotnumber][fname_preftype][RIGHT or LEFT only if append_RIGHT_LEFT is marked True, use False to not include][fftype]
PickFile2shotnum05unfilteredRIGHT.txt : for positive source-receiver offsets
PickFile2shotnum05unfilteredLEFT.txt : for negative soutce-receiver offsets

Similarly, the output reciprocal pick files will follow a naming convention specified in the RecipPicks_ConfigFile.txt:

[rpname_prarrival][arrivaltype][rpname_preshot][shotnumber][rpftype]
RecipPickFile2shot05.txt

A file of shot locations of latitude, longitude needs to be provided in the [shotlocfile], formatted equivalently to the sample in this directory:
shotnum: '[latitude], [longitude]'

Each shot number in the variable [shotnumlist] in the configuration file should have a location provided in the shot location file. 

Each arrival type if [arrivaltypelist] should be consistently labeled between shots, so arrival type 5 in shot 2 should be the same kind of pick as arrival type 5 on all other shots. 

This script makes a rectangular Earth approximation to calculate distance. For increased accuracy, the script could be modified to use UTM. But for this approximation, the km per degrees latitude should be provided in [latkm] and the km per degrees longitude should be provided in [longkm]. This can be determined with an online calculator such as http://www.csgnetwork.com/degreelenllavcalc.html 
