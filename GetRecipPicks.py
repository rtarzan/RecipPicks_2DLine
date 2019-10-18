#!/usr/bin/python

import sys
import re
import os.path
import math
import numpy

#Generalized reciprocal picking script
#Assumes reciprocal picks are organized with separate file for right and left sides where
#$1 = shot offset
#$2 = unreduced travel time
#$3 = error
#$4 = arrival type (arrivals types need to be self-consistent between different shots)

#Assumes that shots are numbered in order of increasing offset in 2D geometry
#lower-number shots to the LEFT of the higher-number shots
#higher-number shots to RIGHT of lower-number shots

def read_config_file(filename):
  #loads text file to dict w/ format on ea line of varname: varval
  f = open(filename)
  RPvar_dict = {}
  for lines in f:
    items = lines.split(': ', 1)
    RPvar_dict[items[0]] = eval(items[1])
  return RPvar_dict

def return_latlong(shotkey_string, type):
  #initialize value - default = -99999
  locval = -99999
  splitlocstring = shotkey_string.split(', ', 1)
  if type == 'lat':
    locval = splitlocstring[0]
  elif type == 'long':
    locval = splitlocstring[1]
  else:
    print 'error: submitted bad type'
  return locval

def recip_pick_finder(arrivaltype, shotnum):
  #load shot loc file
  RP_dict = read_config_file('RecipPicks_ConfigFile.txt')
  shotloc_dict = read_config_file(RP_dict['shotlocfile'])
  
  #put user-specified shots into shot list
  shotlist = []
  shots = RP_dict['shotnumlist'].split(', ', -1)
  shotnumlat = float(return_latlong(shotloc_dict[shotnum],'lat'))
  shotnumlong = float(return_latlong(shotloc_dict[shotnum],'long'))
  
  #calc distance from shotnum to ea other shot
  dist2shot = []
  for shot in shots:
    if shot == shotnum: #shot = shotnum, move onto next shot and rm from recip shot list
      print ''
    elif shot in shotloc_dict.keys(): #calc distance from shotnum to shot
      rlat = float(return_latlong(shotloc_dict[shot],'lat'))
      rlong = float(return_latlong(shotloc_dict[shot],'long'))
      dy = (shotnumlat-rlat)*float(RP_dict['latkm'])
      dx = (shotnumlong-rlong)*float(RP_dict['longkm'])
      dist = math.pow((math.pow(dy,2)+math.pow(dx,2)),0.5)*1000
      dist2shot.append(dist)
    else:
      print 'Shot ', shot, ' not in shot location file: removing from shot list'
      shots.remove(shot)
  
  #gets recip picks = average all picks at offset equal to dist to shot +/- 1 km
  shots.remove(shotnum) #we don't need reciprocal pick at reference shot location
  shcount = len(shots)

  recippicklist = []
  for shot in range(0, shcount):
    fname = RP_dict['fname_prearrival'] + arrivaltype + RP_dict['fname_preshot'] + shots[shot] + RP_dict['fname_preftype']
    if float(shots[shot])-float(shotnum) < 0:
      dist2shot[shot] = dist2shot[shot]*-1
      if RP_dict['append_RIGHT_LEFT'] == True:
        fname = fname + 'RIGHT' + RP_dict['fftype']
        print 'opening pick file', fname
      elif RP_dict['append_RIGHT_LEFT'] == False:
        fname = fname + RP_dict['fftype']
        print 'opening pick file', fname   
      else:
        print 'error: invalid entry in append_RIGHT_LEFT. Should equal either True or False'
    else:
      if RP_dict['append_RIGHT_LEFT'] == True:
        fname = fname + 'LEFT' + RP_dict['fftype']
        print 'opening pick file', fname
      elif RP_dict['append_RIGHT_LEFT'] == False:
        fname = fname + RP_dict['fftype']
        print 'opening pick file', fname   
      else:
        print 'error: invalid entry in append_RIGHT_LEFT. Should equal either True or False'
  
    #load pickfile fname into a list of tuples to get recip pick
    allpicklist = []
    for line in open(fname):
      allpicklist.append(tuple(line.strip().split()))
    
    #use list to get the mean for picks in offset range
    offmin = -dist2shot[shot] + 1000 #recip offset - 1 km
    offmax = -dist2shot[shot] - 1000 #recip offset + 1 km
    a = [float(pick[1]) for pick in allpicklist if offmin>float(pick[0])>offmax]
    
    if a != []: recippicklist.append((dist2shot[shot], numpy.mean(a)))
    
  #writes recip picks to appropriately named text file
  print recippicklist
  if recippicklist != []:
    rpname = RP_dict['rpname_prarrival']+arrivaltype+RP_dict['rpname_preshot']+shotnum+RP_dict['rpftype']
    print 'writing reciprocal picks to file', rpname
    open(rpname, 'w').write('\n'.join('{} \t {}'.format(rpick[0], rpick[1]) for rpick in recippicklist))

def main():
 #read in file of user-specified variables
 RP_dict = read_config_file('RecipPicks_ConfigFile.txt')
 shots = RP_dict['shotnumlist'].split(', ', -1)
 picktype = RP_dict['arrivaltypelist'].split(', ', -1)
 
 for shot in shots:
   for phase in picktype:
     recip_pick_finder(phase, shot)
 
 #test case to be replaced later by what's in RecipPicks_ConfigFile
 #recip_pick_finder('1', '08')
 #recip_pick_finder('5', '08')
 #recip_pick_finder('6', '08')
 
if __name__ == '__main__':
  main()