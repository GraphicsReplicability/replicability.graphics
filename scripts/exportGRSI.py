import csv,os,sys, json,re,codecs
#from pyaltmetric import Altmetric

# importing shutil module
import shutil

def message(variant,doiclean):
 return """Dear author,%0D%0A%0D%0A
you receive this message because you co-authored a TOG/Siggraph paper entitled \""""+ variant['Title']+"""\"  and released the source code at """+ variant['Code URL']+"""%0D%0A
An independent team of experts has successfully evaluated your code for replicability (see https://replicability.graphics/papers/"""+doiclean+"""/).%0D%0A%0D%0A

I herewith invite you to submit your code to the Graphics Replicability Stamp Initiative.%0D%0A
Since replicability was already assessed, your submission will be accepted without any further review.%0D%0A
Upon acceptance, your work will gain a significant visibility because:%0D%0A
(1) the PDF of your TOG paper on ACM Digital Library will be decorated with a replicability badge (see https://dl.acm.org/journal/tog/replicability)%0D%0A
(2) your code will be directly accessible from your paper entry on ACM Digital Library%0D%0A
(3) your code will be listed on the GRSI Website at http://www.replicabilitystamp.org%0D%0A
%0D%0A
You are only required to:%0D%0A
1) add the attached "replicability_instructions.html" file within the root of your git repository;%0D%0A
2) add a proper license file to the root of your git repository (see https://choosealicense.com/).%0D%0A
%0D%0A
When ready, please submit your code here: http://www.replicabilitystamp.org/submissionform.html%0D%0A
%0D%0A
Looking forward to receive your submission!%0D%0A
Best regards,%0D%0A
Marco Attene%0D%0A
GRSI General Chair%0A
"""

messageSubject="""Your TOG paper is eligible for receiveing the Graphics Replicability Stamp"""

def makeA(url):
  return "<a href='"+url+"'>"+url+"</a>"

with open(sys.argv[1]) as json_file:
   fulldata = json.load(json_file)
   line_count = 0


   print("<html><head></head><body>")
   print("<table border=1><tr><th>Year</th><th>Title</th><th>DOI</th><th>Score</th><th>Type</th><th>Code URL</th><th>License</th><th>RG URL</th><th>Go</th><tr>")
   cpt=0;
   for paper in fulldata:
    for variant in paper:
      doi = variant['DOI']
      doiclean = re.sub('/', '-', doi)
      if variant["Is master variant (boolean)"]:
        if variant['Code available (boolean)'] and variant['Replicate paper results score {0=NA, 1,2,3,4,5}'] !="" and variant['Replicate paper results score {0=NA, 1,2,3,4,5}']>=4:
          print("<tr><td>"+str(variant['Year'])+"</td><td>"+variant["Title"]+"</td><td>"+variant["DOI"]+"</td><td>"+str(variant['Replicate paper results score {0=NA, 1,2,3,4,5}'])+"</td><td>"+variant['Software type {Code, Binary, Partial Code}']+"</td><td>"+makeA(variant['Code URL'])+"</td><td>"+variant['Code License (if any)']+"</td><td>"+"<a href='https://replicability.graphics/papers/"+doiclean+"/'>https://replicability.graphics/papers/"+doiclean+"/</td><td><button type='button'><a href='mailto:?cc=jaiko@ge.imati.cnr.it&subject="+messageSubject+"&body="+message(variant,doiclean)+"'>Mail</a></button></td></tr>")
          cpt+=1
      
   print("</table></body></html>")

