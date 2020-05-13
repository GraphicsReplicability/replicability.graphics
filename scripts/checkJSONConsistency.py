from __future__ import print_function
import csv,os,sys, json,re,codecs,datetime
from difflib import SequenceMatcher

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

    
def check(text):
 if text!="":
   eprint(text)
   os._exit(42)

#######################################
def checkYear(variant):
  if variant['Year'] < 2000 or variant['Year'] > 2048:
    return '[Year check] problem with the following year: '+ str(variant['Year'])
  return ""

def checkTopics(variant):
  listTopics = {"Rendering", "Animation and Simulation", "Geometry", "Images", "Virtual Reality", "Fabrication"}
  if not(variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'] in listTopics):
    return '[Topic check] The following topic is not in {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}: '+ str(variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'])
  return ""

 
def checkScore(variant,score):
  if variant[score]== "":
    return ""
  if variant[score] < 0 or variant[score] > 5:
    return '[Score check] problem with the following score: '+ score+', I read  '+str(variant[score])
  return ""

def checkTime(variant,score):
 if variant[score] < 0 or variant[score] > 10:
  return '[Time check] problem with the time (must be in [0,10]): '+str(variant[score])
 return ""

def checkCodeURL(variant):
  if variant["Code available (boolean)"] == True and variant["Code URL"]=="":
   return '[Code URL check] If code is provided (boolean), an URL must be given'
  return ""

def checkCodeType(variant):
  if variant["Code available (boolean)"] == True and variant["Software type {Code, Binary, Partial Code}"]=="":
   return '[Code type check] If code/software is provided (boolean), a type must be given'
  return ""

#######################################
def testMaster(paper):
  errCode=""
  cpt=0;
  for variant in paper:
    if variant['Is master variant (boolean)'] == True:
      cpt = cpt + 1

    
    check(checkYear(variant))
    check(checkTopics(variant))
    check(checkCodeURL(variant))
    check(checkCodeType(variant))
    check(checkScore(variant,"Dependencies score {0=NA, 1,2,3,4,5}"))
    check(checkScore(variant,"Build/configure score {0=NA, 1,2,3,4,5}"))
    check(checkScore(variant,"Fixing bugs score (if any) {0=NA, 1,2,3,4,5}"))
    check(checkScore(variant,"Replicate paper results score {0=NA, 1,2,3,4,5}"))
    check(checkScore(variant,"Adaptability score to other contexts {0=NA, 1,2,3,4,5}"))
    check(checkTime(variant,"Time spent for the test (code download to first successful run, [0,10], 10min slots, 100min max)"))

  if cpt != 1:
    errCode = "[Master Variant Test] There is not exactly one master variant for this paper"
    eprint(errCode)
    
  check(errCode)

#######################################

def checkJSON(paperJSON):
  paper = json.load(open(paperJSON))
  testMaster(paper)

for i in range(1, len(sys.argv)):
  eprint(" ======= Checking the content of the JSON " + sys.argv[i])
  checkJSON(sys.argv[i])
