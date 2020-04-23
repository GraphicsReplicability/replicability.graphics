import csv,os,sys, json,re,codecs
#from pyaltmetric import Altmetric

# importing shutil module
import shutil


def thumbExists(pathPages,doiclean):
  if os.path.isfile(pathPages+doiclean + '/'+ doiclean+'-thumb.png'):
    return True;
  return False


def thumbSmallExists(pathPages,doiclean):
  if os.path.isfile(pathPages+doiclean + '/'+ doiclean+'-thumb-small.png'):
    return True;
  return False


def authorsExists(pathPages,doiclean):
  if os.path.isfile(pathPages + doiclean + '/'+ doiclean+'-metadata.json'):
    return True;
  return False

def pngReduce(pathPages,doi,doiclean,row):
  cmd = 'cd '+pathPages+'/'+doiclean + ' && convert -geometry 15% '+ doiclean+'-thumb.png '+ doiclean+'-thumb-small.png'
  os.system(cmd)
  return True
  
def getThumbnail(pathPages,doi,doiclean,row):
  if row['PDF URL']=="":
    return False
  if thumbExists(pathPages,doiclean):
    #print("      skipping download.. file already exists")
    return True
  cmd = 'cd '+pathPages+' && mkdir ' + doiclean
  os.system(cmd)
  cmd = 'cd '+pathPages+'/'+doiclean + ' && curl "'+row['PDF URL'] + '" --output preprint.pdf '
  os.system(cmd)
  cmd = 'cd '+pathPages+'/'+doiclean + ' && gm convert "preprint.pdf[0]" '+ doiclean+'-thumb.png'
  os.system(cmd)
  cmd = 'rm '+pathPages+'/'+  doiclean+'/*.pdf'
  os.system(cmd)
  return True

def getAuthors(pathPages,doi,doiclean):
  cmd = 'cd '+pathPages+' && mkdir ' + doiclean
  os.system(cmd)
  filename = pathPages + doiclean + '/'+ doiclean+'-metadata.json'
  if os.path.isfile(filename):
    #print("      skipping download.. file already exists")
    with open(filename) as f:
      data = json.load(f)
      return data['message']['author']
  else:
    cmd = 'curl -s "https://api.crossref.org/works/'+ doi + '" > tmpDOI.json'
    os.system(cmd)
    with open("tmpDOI.json") as f:
      data = json.load(f)
      fout = codecs.open(filename,"w+","UTF-8")
      json.dump(data, fout,indent=4)
      return data['message']['author']



with open(sys.argv[1]) as json_file:
   fulldata = json.load(json_file)
   line_count = 0
  
   pathPages='tmp/papers/'
   cmd = "mkdir  tmp/papers"
   os.system(cmd)
   cpt=0;
   for paper in fulldata:
    for variant in paper:
      if isinstance(variant, str):
        print("Oops.. the variant is a string...")
      else:
        if isinstance(variant, list):
           print("Oops.. the variant is a list...")
        else:
          doi = variant['DOI']
          doiclean = re.sub('/', '-', doi)
          #print("Processing "+doiclean)
          
          if not(thumbExists(pathPages,doiclean)):
           getThumbnail(pathPages,doi,doiclean,variant)

          if not(thumbSmallExists(pathPages,doiclean)):
            pngReduce(pathPages,doi,doiclean,variant)
            
          if not(authorsExists(pathPages,doiclean)):
           authors = getAuthors(pathPages,doi,doiclean)
      cpt+=1
      
   print("Number of entries = "+str(cpt))

