from __future__ import print_function
import csv,os,sys, json,re,codecs,datetime
from difflib import SequenceMatcher

###########################

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

    
def check(text):
 if text!="":
   fout = open("error.log", "a")
   errorDetected=True
   eprint(text)
   fout.write(text+'\n')

#######################################

def checkVariant(variant):
  if not("Variant name" in variant):
    return '[Variant name] A variant name must be given'
  return ''

def checkYear(variant):
  if variant['Year'] < 2000 or variant['Year'] > 2048:
    return '[Year check] problem with the following year: '+ str(variant['Year'])
  return ""

def checkTopics(variant):
  listTopics = {"Rendering", "Animation and Simulation", "Geometry", "Images", "Virtual Reality", "Fabrication"}
  if not(variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'] in listTopics):
    return '[Topic check]{Variant: '+variant["Variant name"]+'} The following topic is not in {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}: '+ str(variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'])
  return ""
 
def checkScore(variant,score):
  if variant[score]== "":
    return ""
  if type(variant[score])==str:
    return  '[Score check]{Variant: '+variant["Variant name"]+'} the score '+variant[score]+' must be a number, not a string'
  if variant[score] < 0 or variant[score] > 5:
    return '[Score check]{Variant: '+variant["Variant name"]+'} problem with the following score: '+ score+', I read  '+str(variant[score])
  return ""

def checkTime(variant,score):
 if variant[score] < 0 or variant[score] > 10:
  return '[Time check]{Variant: '+variant["Variant name"]+'} problem with the time (must be in [0,10]): '+str(variant[score])
 return ""

def checkPDFURL(variant):
 if variant["PDF on the authors' webpage / institution (boolean)"] or variant["PDF on Arxiv or any openarchive initiatives (boolean)"]:
     if variant['PDF URL']=="":
      return '[PDF ULR Check]{Variant: '+variant["Variant name"]+'} The PDF being available (either on the author webpage or arxiv/OAI), the PDF URL cannot be empty'
 return ""

def checkCodeURL(variant):
  if variant["Code available (boolean)"] == True and variant["Code URL"]=="":
   return '[Code URL check]{Variant: '+variant["Variant name"]+'} If code is provided (boolean), a URL must be given'
  return ""

def checkArxiv(variant):
  if variant["PDF on Arxiv or any openarchive initiatives (boolean)"] == True and variant["Arxiv/OAI page URL"]=="":
   return '[Arxiv URL check]{Variant: '+variant["Variant name"]+'} If the paper is available on Arxiv/OAI, a URL must be given'
  return ""

def checkCodeType(variant):
  if variant["Code available (boolean)"] == True and variant["Software type {Code, Binary, Partial Code}"]=="":
   return '[Code type check]{Variant: '+variant["Variant name"]+'} If code is provided (boolean), a software type  must be given'
  return ""

def checkCodeType(variant):
  if variant["Code available (boolean)"] == True and variant["Software type {Code, Binary, Partial Code}"]=="":
   return '[Code type check]{Variant: '+variant["Variant name"]+'} If code/software is provided (boolean), a type must be given'
  return ""

def checkAffiliation(variant):
  if not(variant['Co-authors from academia (boolean)'] or variant['Co-authors from industry (boolean)']):
        return '[Affiliation check]{Variant: '+variant["Variant name"]+'} Both "Co-authors from academia (boolean)" and "Co-authors from industry (boolean)" cannot be false'
  return ""


#######################################
def testMaster(paper):
  errCode=""
  cpt=0;
  for variant in paper:
    if variant['Is master variant (boolean)'] == True:
      cpt = cpt + 1

    check(checkVariant(variant))
    check(checkYear(variant))
    check(checkTopics(variant))
    check(checkAffiliation(variant))
    check(checkPDFURL(variant))
    check(checkCodeURL(variant))
    check(checkArxiv(variant))
    check(checkCodeType(variant))
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
  try:
     paper = json.load(open(paperJSON))
     testMaster(paper)
  except json.decoder.JSONDecodeError:
     eprint("Could not open or decode the JSON:", paperJSON)
     
errorDetected=False
fout=open("error.log", "w")
fout.write("");
fout.close()

for i in range(1, len(sys.argv)):
  eprint(" ======= Checking the content of the JSON " + sys.argv[i])
  checkJSON(sys.argv[i])
  
  if errorDetected:
    eprint("Error detected, check error.log file")
    os._exit(42)
