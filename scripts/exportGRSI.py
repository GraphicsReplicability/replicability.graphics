import csv,os,sys, json,re,codecs
#from pyaltmetric import Altmetric

# importing shutil module
import shutil



with open(sys.argv[1]) as json_file:
   fulldata = json.load(json_file)
   line_count = 0

   print("Year;Title;DOI;Score;Type;Code URL;License;RG URL")
   cpt=0;
   for paper in fulldata:
    for variant in paper:
      doi = variant['DOI']
      doiclean = re.sub('/', '-', doi)
      if variant["Is master variant (boolean)"]:
        if variant['Code available (boolean)'] and variant['Replicate paper results score {0=NA, 1,2,3,4,5}'] !="" and variant['Replicate paper results score {0=NA, 1,2,3,4,5}']>=4:
          print(str(variant['Year'])+";"+variant["Title"]+";"+variant["DOI"]+";"+str(variant['Replicate paper results score {0=NA, 1,2,3,4,5}'])+";"+variant['Software type {Code, Binary, Partial Code}']+";"+variant['Code URL']+";"+variant['Code License (if any)']+";https://replicability.graphics/papers/"+doiclean+"/")
          cpt+=1
      

