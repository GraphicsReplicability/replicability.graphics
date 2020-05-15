import csv,os,sys, json,re,codecs
import hashlib
import shutil
from collections import OrderedDict
import datetime

def genChartHeader(f):
    f.write("""
    <div class="row">
    <div class="column2 chart-container" style="position: relative; height:40vh; width:30vw">
    <canvas width="300" height="250" id="myChart" class="chartjs-render-monitor"></canvas>
    </div>
    """)


def processString(s):
    if s =="":
      return "0"
    else:
      return s

def genChart(f,variant,tabid):
    f.write("""<div id="review-%d">""" % (tabid))
    f.write("""<h2>Information</h2>""")

    if variant['Is variant deprecated (boolean)']==True:
        f.write('<ul class="publist-inline-empty-dark"><li>This variant has been marked as deprecated (either the code or the build test have changed)</li></ul>')

    f.write("""<ul>""")
    f.write('<li><span class="family">Paper topic</span>: '+ variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'] + '</li>\n')
    f.write('<li><span class="family">Software type</span>: '+ variant['Software type {Code, Binary, Partial Code}'] + '</li>\n')
    f.write('<li><span class="family">Able to run a replicability test</span>: '+ str(variant["Able to perform a replicability test (boolean)"]) + '</li>\n')
    f.write('<li><span class="family">Replicability score</span>: '+ str(variant['Replicate paper results score {0=NA, 1,2,3,4,5}']) + '</li>\n')

    f.write('<li><span class="family">Software language</span>: '+ variant["Software language"] + '</li>\n')
    f.write('<li><span class="family">License</span>: '+ variant["Code License (if any)"] + '</li>\n')
    f.write('<li><span class="family">Build mechanism</span>: '+ variant["Build/Configure mechanism"] + '</li>\n')
    f.write('<li><span class="family">Dependencies</span>: '+ variant["Dependencies"] + '</li>\n')
    f.write('<li><span class="family">Documentation score</span> {0,1,2}: '+ str(variant["Documentation score {0=NA,1,2,3}"]) + '</li>\n')
 #   f.write('<li><span class="family">Google Scholar Citation</span> ('+ row["Timestamp"] +'):   '+ str(row["Citation count (google scholar)"]) + '</li>\n')
    f.write('<li><span class="family">Reviewer</span>: '+ re.sub('>','&gt;',re.sub('<','&lt;',variant['Reviewer name'])) + '</li>\n')
    f.write('<li><span class="family">Time spent for the test (build->first run, timeout at 100min)</span>: '+ str(variant["Time spent for the test (code download to first successful run, [0,10], 10min slots, 100min max)"]*10) + 'min</li>\n')

    f.write('</ul><h2>Source code information</h2>\n<ul>')
    f.write('<li><span class="family">Code URL</span>:  <a href="'+ variant["Code URL"] + '">'+variant["Code URL"]+'</a></li>\n')
    if variant['Code URL2']!="":
        f.write('<li><span class="family">Code URL 2</span>: <a href="'+ variant["Code URL2"] + '">'+variant["Code URL2"]+'</a></li>\n')
    if variant['MD5 sum (for archives)']!="":
        f.write('<li><span class="family">MD5 hash of the code archive</span>: '+ variant["MD5 sum (for archives)"] + '</li>\n')
    if variant['git/hg/svn commit hash or revision number']!="":
           f.write('<li><span class="family">Git commit hash</span>: '+ variant["git/hg/svn commit hash or revision number"] + '</li>\n')
    if variant['git/hg/svn commit hash or revision number URL2']!="":
         f.write('<li><span class="family">Git commit hash for the second repository</span>: '+ variant["git/hg/svn commit hash or revision number URL2"] + '</li>\n')
    if variant['Software Heritage permalink']!="":
           badgeSWH = re.sub('.org/','.org/badge/',variant['Software Heritage permalink'])
           f.write('<li><span class="family">Software Heritage link</span>: <a href="'+ variant['Software Heritage permalink'] + '"><img src="'+badgeSWH+'"></a></li>\n')


    f.write('</ul><h2>Comments</h2><pre>'+  re.sub('>','&gt;',re.sub('<','&lt;',variant['Build instructions/comments'])) + '</pre>')
    
    if variant['Misc. comments']:
      f.write("<h2>Misc. comments</h2>\n")
      f.write("<pre>" + re.sub('>','&gt;',re.sub('<','&lt;',variant['Misc. comments']))+"</pre>")
	
    f.write("</div>")

def genChartNoTest(f,variant,tabid):
    f.write("""<div id="review-%d">""" % (tabid))
    f.write("""<h2>Information</h2>""")
    f.write("""<ul>""")
    f.write('<li><span class="family">Paper topic</span>: '+ variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'] + '</li>\n')
    val = variant["Able to perform a replicability test (boolean)"]
    if val==False:
      val = "No"
    else:
      val = "Yes"
    f.write('<li><span class="family">Able to run a replicability test</span>: '+ val + '</li>\n')
   # f.write('<li><span class="family">Google Scholar Citation</span> ('+ row["Timestamp"] +'): '+ str(row["Citation count (google scholar)"]) + '</li>\n')
    f.write('<li><span class="family">Reviewer</span>: '+ str(variant['Reviewer name']) + '</li>\n')
    f.write('</ul>')

    ##switch pseudo
    f.write("We haven't found any source code from the authors.<br><br>")

    if not(variant['Code available (boolean)']) and variant['If code not available, pseudo-code available (boolean)']:
      f.write('<span class="family">Some pseudocodes are available in the paper. Could the content be trivially implemented using the given pseudo-code? (1..5)</span>: '+ str(variant['If pseudo-code, could the paper be trivially implemented? {0..4}']) + '\n')
    
    if variant['Misc. comments']:
      f.write("<h2>Misc. comments</h2>\n")
      f.write("<pre>" + re.sub('>','&gt;',re.sub('<','&lt;',variant['Misc. comments']))+"</pre>")
	
    f.write("</div>")


def genChartFooter(f,paper):
    f.write("""
    </div>
    </div>
    </div>
        <script>
 	  var color = Chart.helpers.color;
          var colorNames = Object.keys(window.chartColors);
          var ctx = document.getElementById('myChart');
          var myChart = new Chart(ctx, {
              type: 'polarArea',
              data: {
                labels: ['Dependencies', 'Build / Configure', 'Fixing bugs', 'Easy to adapt', 'Can replicate paper results'],""")
    #else:
    #    f.write("""labels: ['Dependencies', 'Build / Configure', 'Easy to adapt', 'Can replicate paper results'],""")


    f.write("""
                     datasets: [""")
    COLORS = [ 'rgba(255, 99, 132)',
	       'rgba(255, 159, 64)',
	       'rgba(255, 205, 86)',
	       'rgba(75, 192, 192)',
	       'rgba(54, 162, 235)',
	       'rgba(153, 102, 255)',
	       'rgba(201, 203, 207)']
    COLORSB = [ 'rgba(255, 99, 132,0.0)',
	       'rgba(255, 159, 64,0.)',
	       'rgba(255, 205, 86,0.)',
	       'rgba(75, 192, 192,0.)',
	       'rgba(54, 162, 235,0.)',
	       'rgba(153, 102, 255,0.)',
	       'rgba(201, 203, 207,0.)']

    for cpt, var in enumerate(paper):
        feed =  processString(str(var['Dependencies score {0=NA, 1,2,3,4,5}']))
        feed+=  processString(str(var['Build/configure score {0=NA, 1,2,3,4,5}']))
        feed+=  processString(str(var['Fixing bugs score (if any) {0=NA, 1,2,3,4,5}']))
        feed+=  processString(str(var['Adaptability score to other contexts {0=NA, 1,2,3,4,5}']))
        feed+=  processString(str(var['Replicate paper results score {0=NA, 1,2,3,4,5}']))
        data="["+str(feed[0])+ ","+str(feed[1])+","+str(feed[2])+","+str(feed[3])+","+str(feed[4])+"]"
        bw = str(4) if cpt==0 else str(1)

        f.write("""{
                      label: 'Variant -- \""""+ var['Variant name']+"""\" (the higher, the better,  {1..5}, 0=N/A )',
                      showLine: false,
           """)
        if (cpt == 0):
            f.write("""
                      borderColor: "#000",
                      borderWidth: 2,
                      backgroundColor: [
                          'rgba(255, 99, 132,.6)',
                          'rgba(255, 159, 64,.6)',
                          'rgba(255, 205, 86,.6)',
                          'rgba(75, 192, 192,.6)',
                          'rgba(54, 162, 235,.6)',
                      ],
           """)
        else :
            f.write("""
                      borderColor: "#fff",
                      borderWidth: 0,
                      backgroundColor: [
                          'rgba(255, 99, 132,0.2)',
                          'rgba(255, 159, 64,0.2)',
                          'rgba(255, 205, 86,0.2)',
                          'rgba(75, 192, 192,0.2)',
                          'rgba(54, 162, 235,0.2)',
                      ],
           """)
        f.write("           data: "+data+"")
        f.write("""
                  },""")
    f.write("""
                  ]
              },
              options: {
  scale: {
      ticks: {
          suggestedMin: 0,
          suggestedMax: 5,
          stepSize: 1
      }
  }
}
          });

        </script>
    """)


def genBadges(row):
  ##Has Code
  attribute=''
  signature =[0,0,0,0,0,0,0,0]
  scorePseudocode = 0
  if row['If pseudo-code, could the paper be trivially implemented? {0..4}']!="":
     scorePseudocode=row['If pseudo-code, could the paper be trivially implemented? {0..4}']
  testRun=row["Able to perform a replicability test (boolean)"]
  hasOpenAccessPDF = row['ACM Open Access (boolean)']
  hasCode = row['Code available (boolean)']
  hasPseudoCode= row['If code not available, pseudo-code available (boolean)']

  doi = row['DOI']
  doiclean = re.sub('/', '-', doi)
  if hasCode:
     if row['Replicate paper results score {0=NA, 1,2,3,4,5}'] >=4:
      attribute = '<i class="fas fa-circle graphcol0" style="font-size:150%;color:#0868ac;" title="code available and we were able to reproduce most results (score >= 4)"></i>'
      signature[0] += 1
     else:
      if row['Replicate paper results score {0=NA, 1,2,3,4,5}'] > 1:
       attribute = '<i class="fas fa-circle graphcol1" style="font-size:150%;color:#43a2ca;" title="code available and we were able to reproduce some results"></i>'
       signature[1] += 1
      else:
       attribute = '<i class="fas fa-circle graphcol2" style="font-size:150%;color:#7bccc4;" title="code available but we weren\'t able to reproduce any results (technical issue, device specific, repl. score <= 1)"></i>'
       signature[2] += 1

  else:
    if hasPseudoCode:
      if scorePseudocode>=4:
        attribute = '<i class="fas fa-map-marker graphcol3"  style="font-size:150%;color:rgb(95,44,102);" title="only pseudo-code available in the paper with simple implementation (score >=4)"></i>'
        signature[3] += 1

      else:
        attribute = '<i class="fas fa-map-marker graphcol4"  style="font-size:150%;color:rgb(186,147,186);" title="only pseudo-code available in the paper"></i>'
        signature[4] += 1


  ###
  if hasCode:
     if not testRun:
      if row['Replicate paper results score {0=NA, 1,2,3,4,5}'] > 0:
        print( "[WARNING] Has Code, test not run but repl. score >0 [ https://replicability.graphics/papers/"
               + doiclean+"/index.html  "+ row['DOI'] + "]" )

   ##PDF not available
  if hasOpenAccessPDF:
       attribute += ' <i class="fas fa-splotch graphcol5"  style="font-size:150%;color:#1b9e77;" title="PDF available as an ACM Open Access document"></i>'
       signature[5] += 1

  if row["PDF on the authors' webpage / institution (boolean)"]==False  and row['PDF URL']=="" and row['PDF on Arxiv or any openarchive initiatives (boolean)']==False:
     attribute += ' <i class="fas fa-square graphcol7"  style="font-size:150%;color:#d95f02;" title="PDF only available on the Digital Library (not Open Access)"></i>'
     signature[7] += 1
  else:
     attribute += ' <i class="fas fa-square graphcol6"  style="font-size:150%;color:#7570b3;" title="Preprint PDF available (author web page, project page, institution page, arxiv...)"></i>'
     signature[6] += 1

  return [attribute,signature]


def generatePage(f,pathPages,variant,doi,doiclean,authors,tabid):
 title = variant['Title']
 badgeRep = genBadges(variant)
 PDFURL = variant['PDF URL']
 ProjectURL = variant['Project URL']
 code1 = variant['Code URL']
 code2 = variant['Code URL2']
 arxiv = variant['Arxiv/OAI page URL']
 TestRun=variant["Able to perform a replicability test (boolean)"]
 hasCode = variant['Code available (boolean)']

 if hasCode:
     genChart(f,variant,tabid)
 else:
     genChartNoTest(f,variant,tabid)

def delKey(paper,key):
  for var in paper:
      if key in var:
        del var[key]

def generateAllPages(pathPages,paper):

 variant=[]
 for var in paper:
   if isinstance(var, str):
     print("Oops.. the variant is a string...")
   else:
     if isinstance(var, list):
       print("Oops.. the variant is a list...")
     else:
      if var['Is master variant (boolean)'] == True:
         variant = var

 doi = variant['DOI']
 doiclean = re.sub('/', '-', doi)

 ##Export without comments
 fout=codecs.open(pathPages+doiclean+'/replicability.json', "w+","UTF-8")
 json.dump(paper, fout,indent=4)

 authors=getAuthors(pathPages,doi,doiclean)
 title = variant['Title']
 badgeRep = genBadges(variant)
 PDFURL = variant['PDF URL']
 ProjectURL = variant['Project URL']
 code1 = variant['Code URL']
 code2 = variant['Code URL2']
 arxiv = variant['Arxiv/OAI page URL']
 TestRun=variant["Able to perform a replicability test (boolean)"]
 hasCode = variant['Code available (boolean)']
 f=codecs.open(pathPages+'/'+doiclean+'/index.html', "w+","UTF-8")
 f.write("""<html><head><meta charset="utf-8">
 <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
 <script src="../../assets/js/chart-utils.js"></script>
<link rel="stylesheet"
       href="../../assets/css/default.min.css">
 <script src="../../assets/js/highlight.min.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
 <link href="../../assets/css/all.css" rel="stylesheet">
 <link rel="stylesheet" href="../../assets/css/customstyle.css">
 <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretty-checkbox@3.0/dist/pretty-checkbox.min.css">\n
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  var currentReviewId = 0;

  $( function() {
    $( "#tabs" ).tabs({
    activate: function (event, ui) {
        var reviewId = parseInt(event.currentTarget.id.substring(6));

        [myChart.data.datasets[0].data, myChart.data.datasets[currentReviewId].data] =
 [myChart.data.datasets[currentReviewId].data, myChart.data.datasets[0].data];

        currentReviewId = reviewId-1;

        [myChart.data.datasets[0].data, myChart.data.datasets[currentReviewId].data] =
 [myChart.data.datasets[currentReviewId].data, myChart.data.datasets[0].data];

        myChart.update(0);
    }
  });
  } );
  </script></head>\n<body>
 """)

 f.write("""<html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3"></script>
  <link rel="stylesheet"
        href="../../assets/css/default.min.css">
  <script src="../../assets/js/highlight.min.js"></script>
  <script>hljs.initHighlightingOnLoad();</script>
  <link href="../../assets/css/all.css" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/customstyle.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretty-checkbox@3.0/dist/pretty-checkbox.min.css">\n

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-164636527-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-164636527-1');
</script>



  </head>\n<body>
  """)
 f.write('<ul class="publist-inline" style="text-align:left;"><li class="web"><a href="../../browse.html">< The Data</a></ul>')
 f.write('<h1 class="title">'+title+" "+ badgeRep[0]+'</h1>')

 f.write('<ul class="authors">\n')
 for x in authors:
     f.write('<li> '+x['given']+' '+ '<span class="family">'+x['family']+'</span></li>\n')
 f.write('</ul>\n')
 f.write('<center> SIGGRAPH '+ str(variant['Year']) +'</center>')

  #f.write('<img src="'+ stats['images']['medium']+'" />')
 f.write('<ul class="publist-inline">\n');
 f.write('<li class="web"> <i class="fas fa-globe-americas"></i> <a href="https://doi.org/'+doi+'">ACM</a></li>\n')

 if PDFURL != '' :
     f.write('<li class="pdf"> <i class="far fa-file-pdf"></i> <a href="'+PDFURL+'">preprint</a></li>\n')

 if ProjectURL != '' :
          f.write('<li class="web"> <i class="fas fa-globe-americas"></i> <a href="'+ProjectURL+'">Project page</a></li>\n')

 if code1 != '':
          f.write('<li class="web"> <i class="far fa-file-alt"></i> <a href="'+code1+'">Code</a></li>\n')

 if code2 != '':
          f.write('<li class="web"> <i class="far fa-file-alt"></i> <a href="'+code2+'">Code 2</a></li>\n')
 if arxiv != '':
          f.write('<li class="web"> <i class="fas fa-university"></i> <a href="'+arxiv+'">arXiv or openarchive initiative</a></li>\n')


 f.write('<li class="web"> <i class="fas fa-database"></i> <a href="'+doiclean+'-metadata.json">DOI Metadata</a></li>\n')
 f.write('</ul>\n');

 f.write('<center><img width="300" src="'+doiclean+'-thumb.png"></img></center>')

 # f.write('<h4>Variant: '+variant['variant name']+'</h4>')
 f.write('<br><br><ul class="publist-inline" style="text-align:left;font-size:100%"><li > <i ></i> <a href="replicability.json">Download complete data for this entry</a></li></ul>')


 #print(pathPages+'/'+doiclean+'/index.html     '+variant['Title'])

 #Generate header
 genChartHeader(f)

 #Generate the master
 f.write('''
    <div class="column2">
    <h2>Reviews</h2>
       <div id="tabs">
          <ul>''')
 for varid, var in enumerate(paper):
    if var['Is variant deprecated (boolean)']==False:
        f.write("             <li><a href=\"#review-%d\">%s</a></li>\n" % (varid+1, var['Variant name']))
    else:
        f.write("             <li><a style='color:gray;text-decoration:line-through;' href=\"#review-%d\">%s</a></li>\n" % (varid+1, var['Variant name']))

 f.write("             <li><a href=\"#review-%s\">&#43;</a></li>\n" % (len(paper)+1))
 f.write("</ul>")


 #and the remaining ones
 for varid, var in enumerate(paper):
    generatePage(f,pathPages,var,doi,doiclean,authors,varid+1)

 f.write('''<div id=review-%s>
           <p> If you want to contribute with another review, please follow <a href="../../index.html#contribute">these instructions</a>. </p>

            <p>Please consider to cut/paste/edit the <a href="replicability.json">raw JSON data</a> attached to this paper.</a></p>
            </div>
            '''% (len(paper)+1));

 f.write('</div></div>')


 #and the JS for the plot
 genChartFooter(f,paper)

 disqus_url = "https://replicability-siggraph.disqus.com/embed.js" if variant['DOI']=="10.1145/3197517.3201378" else "https://replicability-graphics.disqus.com/embed.js"

 path = "siggraph-"+str(variant['Year'])+'/'
 f.write('</code></pre>')
 f.write("</body>")
 f.write("<div style=\"height:30px;display:block;\"></div>")
 f.write("""<div id="disqus_thread"></div>
 <script>
 /**
 *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
 *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
 /*
 var disqus_config = function () {
 this.page.url = """+"'https://replicability.graphics'"+""";  // Replace PAGE_URL with your page's canonical URL variable
 this.page.identifier = '""" + doiclean+ """'; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
 };
 */
 (function() { // DON'T EDIT BELOW THIS LINE
 var d = document, s = d.createElement('script');
 s.src = '""" + disqus_url  + """';
 s.setAttribute('data-timestamp', +new Date());
 (d.head || d.body).appendChild(s);
 })();
 </script>
 <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>""")

 f.write("</html>")
 f.close()



def thumbExists(pathPages,doiclean):
  if os.path.isfile(pathPages+doiclean + '/'+ doiclean+'-thumb.png'):
    return True;
  return False




def dumpTableHeader(findex):
  findex.write('<table id="myTable" class="display">')
  findex.write('<thead><tr>')
  findex.write('<th></th>')
  findex.write('<th>Title</th>')
  findex.write('<th></th>')
  findex.write('<th>PDF</th>')
  findex.write('<th>Year</th>')
  findex.write('<th>Topic</th>')
  findex.write('<th>Code available</th>')
  findex.write('<th>Replicability score</th>')
  findex.write('<th>Pseudocode only</th>')
  findex.write('<th>Pseudocode score</th>')
  findex.write('<th>Doc. score</th>')
  findex.write('<th>Altmetric score</th>')
  findex.write('</tr></thead>\n<tbody>')

def dumpTableFooter(findex,topicsGlobal, data):
  findex.write('</tbody></table>')
  findex.write("""<script type="text/javascript" src="assets/js/sortArrays.js"></script>""")
  findex.write("""<script type="text/javascript" src="assets/js/browse-updateViz.js"></script>""")
  findex.write("""
  <script>
  $(document).ready(function() {
    // Setup - add a text input to each footer cell
    //$('#myTable thead tr').clone(true).appendTo('#myTable thead');
    $('#myTable thead tr:eq(0) th').each(function(i) {
      if (i == 1 || i==4 || i==5 || i==7) {
        var title = $(this).text();
        if (i==1) {
          $(this).html('<input type="text" size="40" placeholder="Search by title or author name" />');


          $('input', this).on('keyup change', function() {
            if (table.column(i).search() !== this.value) {
              table
                .column(i)
                .search(this.value)
                .draw();
            }
            updateChartFromData();
          });
        } else {
          if (i==4) {
            $(this).html('<select id="comboyear"><option value="">All Years</option> """)
  for y, d in data["years"].items():
    findex.write('''<option value="'''+ str(y) + '''">'''+ str(y) + '''</option>''')
  findex.write("""</select>');
          }
  """)
  findex.write("else if (i==5)\n")
  topicinput="""$(this).html('<select id="combotopic"><option value="">All Topics</option>"""
  for kw in topicsGlobal:
    if kw != '':
      topicinput += "<option value=\""+kw+"\">"+kw+"</option>"
  topicinput += """</select>');"""
  findex.write(topicinput)
  findex.write("""
          $('select', this).on('keyup change', function() {

            if (table.column(i).search() !== this.value) {
              table
                .column(i)
                .search(this.value)
                .draw();
            }
            updateChartFromData();
          });
        }
      }
    });
  });
  </script>
  """)
def getAuthors(pathPages,doi,doiclean):
  filename = pathPages + doiclean + '/'+ doiclean+'-metadata.json'
  if os.path.isfile(filename):
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


def getAltmetric(pathPages,doiclean):
 filename=pathPages+doiclean+"/Altmetric.json"
 if os.path.isfile(filename):
  altm=open(filename)
  for line in altm:
    if line=="Not Found":
      return [-1,"xx","xx"]

    line ="[" + line + "]"
    fout=codecs.open('tmp.json', "w+","UTF-8")
    fout.write(line)
    fout.close()
    tmp=open("tmp.json")
    altmdata = json.load(tmp)
    return [altmdata[0]["score"], altmdata[0]["images"]["small"], altmdata[0]["details_url"]]
 return [-1,"xx","xx"]


def explanationBadges(findex):
    findex.write("""
    <h3 style="text-align:left;">Badges</h3>
    <ul class="publist-inline2" style="font-size:60%">
    <li> <i class="fas fa-circle" style="font-size:150%;color:#0868ac;" title="code available and we were able to reproduce most results (score >= 4)"></i> <b>(C1)</b> code available and we were able to reproduce most results (score >= 4)
    <li> <i class="fas fa-circle" style="font-size:150%;color:#43a2ca;" title="code available and we were able to reproduce some results"></i> <b>(C2)</b> code available and we were able to reproduce some results (score > 1)
    <li> <i class="fas fa-circle" style="font-size:150%;color:#7bccc4;" title="code available but we weren't able to reproduce any results (technical issue, device specific, repl. score <= 1)"></i> <b>(C3)</b> code available but we weren't able to reproduce any results (technical issue, device specific, score <= 1)
    <li> <i class="fas fa-map-marker" style="font-size:150%;color:rgb(95,44,102);" title="only pseudo-code available in the paper with simple implementation (score >=4)"></i> <b>(PC1)</b> only pseudo-code available in the paper with simple implementation (score >=4)
    <li> <i class="fas fa-map-marker" style="font-size:150%;color:rgb(186,147,186);" title="only pseudo-code available in the paper"></i> <b>(PC2)</b> only pseudo-code available in the paper
    <li> <i class="fas fa-splotch" style="font-size:150%;color:#1b9e77;" title="PDF available as an ACM Open Access document"></i> PDF available as an ACM Open Access document
    <li> <i class="fas fa-square" style="font-size:150%;color:#7570b3;" title="Preprint PDF available (author web page, project page, institution page, arxiv...)"></i> Preprint PDF available (author web page, project page, institution page, arxiv...)
    <li> <i class="fas fa-square" style="font-size:150%;color:#d95f02;" title="PDF only available on the Digital Library (not Open Access)"></i> PDF only available on the Digital Library (not Open Access)
    </ul>
    <hr />
    """)

with open(sys.argv[1]) as json_file:
   fulldata = json.load(json_file)

   print("Generating database page")

def write_browse_step1(fbrowse):
   fbrowse.write('''
      <footer>
       <a href="index.html#project" class="button">The Project</a>
       <a href="#data" class="button scrolly">The Data</a>
       <a href="index.html#team" class="button">The Team</a>
       <a href="index.html#contribute" class="button">Contribute</a>
	    </footer>
    </section>
    <!-- First -->
    <section id="data" class="main">
      <header>
        <div class="container">
            <h2>The Data</h2>
   ''')

   explanationBadges(fbrowse)

   fbrowse.write('''
            <div class="row">
                <div class="column2 chart-container">
                    <canvas height="150" id="myChartTopics" class="chartjs-render-monitor"></canvas>
                </div>
                <div class="column2 chart-container">
                    <canvas height="150" id="myChartPdf" class="chartjs-render-monitor"></canvas>
                </div>
            </div>
   ''')
   dumpTableHeader(fbrowse)

def write_browse_step2(fbrowse, data):
   dumpTableFooter(fbrowse,allTopics, data)
   tdy = datetime.datetime.now()
   fbrowse.write('''
            </div>
        </header>
    Last update: '''+ str(tdy) +'''
    </section>
    ''')

def write_index_step1(findex):
   findex.write('''
      <footer>
	<a href="#project" class="button scrolly">The Project</a>
	<a href="browse.html#data" class="button">The Data</a>
        <a href="index.html#team" class="button">The Team</a>
	<a href="#contribute" class="button scrolly">Contribute</a>
     </footer>
    </section>
    ''')
def write_index_step2(findex, data):
   nbReplicable = 0
   for y, d in data["years"].items():
      nbReplicable = d[0] + d[1] + nbReplicable
   findex.write('''
    <!-- First -->
    <section id="project" class="main">
      <header>
	  <h2>The Project</h2>
      </header>
	<div class="container">
	  <p style="text-align:left"> Being able to duplicate published research results is an
        important process of conducting research whether to build upon
        these findings or to compare with them.  This process is
        called &ldquo;replicability&rdquo; when using the original authors'
        artifacts (e.g., code), or &ldquo;reproducibility&rdquo; otherwise
        (e.g., re-implementing algorithms).  Reproducibility and
        replicability of research results have gained a lot of
        interest recently with assessment studies being led in various
        fields, and they are often seen as a trigger for better result
        diffusion and transparency.  In this project, we assess
        replicability in Computer Graphics, by evaluating whether the
        code is available and whether it works properly.  As a proxy
        for this field we compiled, ran and analyzed ''' + str(data["cptHasCode"])+ ''' codes out of
       ''' + str(data["cpt"]) + ''' papers from SIGGRAPH conferences (exhaustive for 2014, 2016 and 2018). In the analysis described in</p>
       <p>
       <ul class="publist-inline-empty-dashed"  style="text-align:left;">
       <li> Nicolas Bonneel, David Coeurjolly, Julie Digne, Nicolas Mellado, <a href="https://replicability.graphics/replicability.pdf"><i><b>Code Replicability in Computer Graphics</b></i> <i class="fas fa-file-pdf"></i></a>, ACM Trans. on Graphics (Proceedings of SIGGRAPH 2020), 39:4,</li></ul></p>

        <p style="text-align:left">we show a clear increase in the number of papers with
        available and operational research codes with a dependency on
        the subfields, and exhibit a correlation between code
        replicability and citation count. </p>

      <p style="text-align:left">This website provides an interactive tool to explore our results and evaluation data.
      It also provides tools to comment on the various codes either as an author or as a user. All materials (data, scripts..) that  have been used to generate these results are available on the  <a
      href="https://github.com/GraphicsReplicability/replicability.graphics"> <img width="20pt" src="images/github.png"/>&nbsp;replicability.graphics
      GitHub project</a>. The website contains the data for all papers in:</p>
      <p> <ul class="publist-inline">
       <li> SIGGRAPH 2014</li>
       <li> SIGGRAPH 2016</li>
       <li> SIGGRAPH 2018</li>
       </ul></p>
       <p style="text-align:left">and partial data for:</p>
       <ul class="publist-inline-empty">
       <li> SIGGRAPH 2019</li>
       </ul>
       <p style="text-align:left">As a long term goal, we would like to collect data for more SIGGRAPH venues, for SIGGRAPH ASIA editions, for ToG papers, and for any other computer graphics events. If you want to help, see <a href="#contribute" class="scrolly">contributions</a>, and check out <a href="https://github.com/GraphicsReplicability/replicability.graphics/blob/master/CONTRIBUTORS.md">the contributors</a>. </p>


     <p style="text-align:left"> Our project aims at providing the
     community with tools to improve Computer Graphics research
     replicability. While the <a
     href="http://ReplicabilityStamp.org" target="_blank">Graphics Replicability Stamp
     Initiative</a> (GRSI) encourages authors to <b>make</b> their resarch
     replicable, in our project we check whether existing research <b>is</b>
     replicable.</p>

      <p style="text-align:left">You can contribute new code analysis for computer graphics
      papers. We're looking forward to your <a href="#contribute" class="scrolly">contributions</a>. You can also <a href="#contact" class="scrolly">contact us</a>.</p>

  </div>
  <div class="container">
     <hr />
     <header>
     <h2 style="text-align:center;">Data Digest</h2>
      </header>

    <div class="row">
        <div class="column2 ">
            <h4 style="text-align:center;">Key numbers</h4>
            <div class="row">
                <div class="column1">
                    Number of papers reviewed: ''' + str(data["cpt"]) + '''
                </div>
            </div>
            <div class="row">
                <div class="column1">
                    Number of reviews: '''+str(data["cptVariants"])+'''
                </div>
            </div>
            <div class="row">
                <div class="column1">
                    Number of papers with code: ''' + str(data["cptHasCode"])+ '''
                </div>
            </div>
            <div class="row">
                <div class="column1">
                    Number of replicable papers: ''' + str(nbReplicable)+ '''
                </div>
            </div>
        </div>
        <div class="column2 chart-container">
            <p style="text-align:center;">Number of review / year of publication</p>
            <canvas height="150" id="myChartYears" class="chartjs-render-monitor"></canvas>
        </div>
    </div>
    <div class="row">
        <div class="column2 chart-container">
            <p style="text-align:center;">Replicability results for reviewed papers</p>
            <canvas height="150" id="myChartTopics" class="chartjs-render-monitor"></canvas>
        </div>
        <div class="column2 chart-container">
            <p style="text-align:center;">PDF accessibility for reviewed papers</p>
            <canvas height="150" id="myChartPdf" class="chartjs-render-monitor"></canvas>
        </div>
    </div>
  </div>

    <script>
    $(document).ready(function(){
    myChartTopics.data.labels =['Most results reproduced',
             'Some results reproduced',
             'Could not reproduce using code',
             'Total (code available)',
             'Total (code not available)',
             'Easy to reproduce using pseudo-code',
             'Hard to reproduce using pseudo-code',
             'Total (only pseudo-code)'];''')
   did = 0
   for y, d in data["years"].items():
        findex.write('''
        myChartTopics.data.datasets.push(myChartGenerateEmpty(''' + str(did) + '''));
        myChartTopics.data.datasets[''' + str(did) + '''].data = [''' + ', '.join(map(str, d)) + '''] ;
        myChartTopics.data.datasets[''' + str(did) + '''].label = ''' + y + ''';
        ''')
        did = did+1
   did = 0
   for y, d in data["yearspdf"].items():
        findex.write('''
        myChartPdf.data.datasets.push(myChartPdfGenerateEmpty(''' + str(did) + '''));
        myChartPdf.data.datasets[''' + str(did) + '''].data = [''' + ', '.join(map(str, d)) + '''] ;
        myChartPdf.data.datasets[''' + str(did) + '''].label = ''' + y + ''';
        ''')
        did = did+1
   findex.write('''
        myChartTopics.update();
        myChartPdf.update();
    });

    var myChartYears = new Chart(document.getElementById('myChartYears'), {
      type: 'horizontalBar',
      data: {
        labels: [''')

   for y in data["years"].keys():
      findex.write("""'""" + y + """',""")

   findex.write('''],
        datasets: [{
           data: [''')
   for y, d in data["years"].items():
      findex.write("""'""" + str(d[3] + d[4]) + """',""")

   findex.write(''']
          }]
      },
      options: {
        legend: {
            display: false,
        }
      }
    });
    </script>

      <div class="content dark style1 featured">
	<div class="container">
	  <div class="row">
	    <div class="col-4 col-12-narrow">
	      <section>
		<span class="feature-icon"><span class="icon
		solid fa-book-open"></span></span>
		<header>
		  <h3><a href="browse.html#data">Explore</a></h3>
		</header>
		<p>Explore the data and our replicability scores</p>
	      </section>
	    </div>
	    <div class="col-4 col-12-narrow">
	      <section>
		<span class="feature-icon"><span class="icon solid fa-microscope"></span></span>
		<header>
		  <h3><a href="#team" class="scrolly">Analyze</a></h3>
		</header>
		<p>Read our Siggraph 2020 paper on 374 analyzed 2014-2016-2018 Siggraph papers.</p>
	      </section>
	    </div>
	    <div class="col-4 col-12-narrow">
	      <section>
		<span class="feature-icon"><span class="icon solid fa-comments"></span></span>
		<header>
		  <h3><a href="#contribute" class="scrolly">Contribute</a></h3>
		</header>
		<p>Add comments or new analyses for Computer Graphics papers.</p>
	      </section>
	    </div>
	    <div class="col-12">
	      <footer>
		<a href="browse.html#data" class="button scrolly">''' + str(data["cptVariants"]) + ''' reviews so far</a>
	      </footer>
	    </div>
	  </div>
	</div>
      </div>
    </section>


    <section id="team" class="main">
        <div class="content dark style2">
            <div class="container">
                <div class="col-4 col-12-narrow">
                <h3>The Team</h3>
                <ul style="text-align:left">
                <li> <a href="https://perso.liris.cnrs.fr/nicolas.bonneel/">Nicolas Bonneel</a> (CNRS, LIRIS, Lyon, France)
                <li> <a href="https://perso.liris.cnrs.fr/david.coeurjolly/">David Coeurjolly</a> (CNRS, LIRIS, Lyon, France)
                <li> <a href="https://perso.liris.cnrs.fr/julie.digne/">Julie Digne</a> (CNRS, LIRIS, Lyon, France)
                <li> <a href="https://www.irit.fr/~Nicolas.Mellado/">Nicolas Mellado</a> (CNRS, IRIT, Toulouse, France)
                </ul>


                <img height="100px" src="images/logo_cnrs.png"/>   &nbsp;&nbsp;&nbsp;  <img height="100px" src="images/logo_liris.png"/> &nbsp;&nbsp;&nbsp; <img height="100px"  src="images/logo_irit.png"/>

                </div>
            </div>
        </div>
    </section>

   	<section id="contribute" class="main">
	  <header>
	    <div class="container">
	      <h2>Contribute</h2>
              <p style="text-align:left">There are several ways in which you can contribute and help us improve Computer Graphics research replicability</p>
              <ul style="text-align:left">
              <li> Add a comment (alternative compilation tricks, details on the code...) via the discussion on each paper page.</li>
              <li> Add a new variant (replicability test), <i>i.e.</i> edit an existing JSON file (see below).
              <li> Add a new entry to the system (new paper), <i>i.e.</i> submit a new JSON file.
              </ul>

                <p style="text-align:left">For the last two cases, you
                can either submit a proper <a
                href="https://github.com/GraphicsReplicability/replicability.graphics/blob/master/template.json">JSON file</a> as a <a
                href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request">pull request</a>
                to this <a href="https://github.com/GraphicsReplicability/replicability.graphics"><img width="20pt" src="images/github.png"/> project</a>, or send the JSON file to <a href="mailto:GraphicsReplicability@liris.cnrs.fr">GraphicsReplicability@liris.cnrs.fr</a>.</p>

                <p style="text-align:left"><strong>Note about self-reviewing</strong>: we accept the reviews provided by the authors of a paper. These reviews will be clearly identified and may be double checked to validate the replicability. If you're an author, please clearly mention it when submitting your review.</p>

                <p style="text-align:left">In our system, the website
                is fully generated from data available on JSON
                documents. You can browse the database on the <a
                href="https://github.com/GraphicsReplicability/replicability.graphics/tree/master/data">github
                project page</a>. Each paper is a single JSON file, named by the paper DOI,
                with multiple "variant" records. Each variant is a
                build test on a specific system, environment or
                reviewer. For example, an article with DOI <b>10.1145/2601097.2601102</b> has a <b>10.1145-2601097.2601102.json</b> file which looks like </p>
                <pre class="prejson">

                [
                  {
                    ....
                    ... data for variant A ...
                    ...
                  },
                  {
                    ....
                    ... data for variant B ...
                    ...
                  },
                  ....
                ]
                </pre>

                <p style="text-align:left">We highly recommend having a look to our <a
                href="https://github.com/GraphicsReplicability/replicability.graphics/blob/master/template.json">template
                JSON</a> with all the explanations about the fields we
                are using.</p>

                <p style="text-align:left">If you have any question,
                feature requests or found any bug, do not hesitate to
                report an <a
                href="https://github.com/GraphicsReplicability/replicability.graphics/issues/new/choose">Issue</a>.
                </p>

                </div>
           </header>
        </section>

    <section id="contact" class="main">
        <div class="content dark style2">
            <div class="container">
                <div class="col-4 col-12-narrow">
	      <h2>Contact us</h2>
	      <p>Drop us an <a href="mailto:GraphicsReplicability@liris.cnrs.fr">email</a> for more information or to let us know what you think.</p>

                </div>
            </div>
        </div>
    </section>
	  </div>
    ''')

with open(sys.argv[1]) as json_file:
   fulldata = json.load(json_file)

   print("Generating webpages")

   line_count = 0
   #topicsGlobal = getAllTopics(fulldata)
   fbrowse = codecs.open('tmp/core-browse.html','w+', "UTF-8")
   findex = codecs.open('tmp/core-index.html','w+', "UTF-8")
   pathPages='tmp/papers/'

   write_browse_step1(fbrowse)
   write_index_step1(findex)

   allTopics = {"Rendering", "Animation and Simulation", "Geometry", "Images","Virtual Reality", "Fabrication"}

   cpt=0;
   cptHasCode=0;
   cptVariants=0
   step2data = dict()

   step2data["years"]   = dict()
   step2data["yearspdf"]   = dict()

   print("Generating index...")
   for paper in fulldata:
     delKey(paper,'##')
     for variant in paper:
      if isinstance(variant, str):
        print("Oops.. the variant is a string...")
      else:
        if isinstance(variant, list):
           print("Oops.. the variant is a list...")
        else:
           cptVariants += 1
           if variant['Is master variant (boolean)'] == True:
              # Cannot use get here, is it does not actually add the default element to the dict
              if str(variant['Year']) not in step2data["years"]:
                step2data["years"][str(variant['Year'])] = [0,0,0,0,0,0,0,0]
              if str(variant['Year']) not in step2data["yearspdf"]:
                step2data["yearspdf"][str(variant['Year'])] = [0,0,0]

              step2dataYear    = step2data["years"][str(variant['Year'])]
              step2dataYearPdf = step2data["yearspdf"][str(variant['Year'])]

              doi = variant['DOI']
              doiclean = re.sub('/', '-', doi)

              authors=getAuthors(pathPages,doi,doiclean)
              authorstring=''
              for x in authors:
               authorstring +=', '+ x['given']+' '+ x['family']
               # remove first comma
              authorstring = authorstring[2:];

              fbrowse.write('<tr class="'+variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}']+' '+str(variant['Year'])+' ">')

              hasCode = ""
              if variant['Code available (boolean)'] == True:
                hasCode = '✔️'
                cptHasCode += 1
                step2dataYear[3] = step2dataYear[3] + 1

              else:
                hasCode = '×'
                step2dataYear[4] = step2dataYear[4] + 1

              hasPseudoCode = variant["If code not available, pseudo-code available (boolean)"]
              if hasPseudoCode==True:
                  hasPseudoCode = '✔️'
                  step2dataYear[7] = step2dataYear[7] + 1
              else:
                  hasPseudoCode = '×'

              paperBadge = genBadges(variant)

              altmetric = getAltmetric(pathPages,doiclean)

              if thumbExists(pathPages,doiclean):
                 fbrowse.write('<td style="text-align:center;vertical-align: middle;"><img class="thumb" src="papers/'+doiclean+'/'+doiclean+'-thumb-small.png"></td>')
              else:
                 fbrowse.write('<td></td>')
              fbrowse.write("<td> <a href=papers/"+doiclean+"/index.html>"+variant['Title']+"</a> "+authorstring+"</td>")
              fbrowse.write("<td>"+paperBadge[0]+" </td>")
              #PDF
              fbrowse.write("<td></td>")
              #Year
              fbrowse.write("<td>"+str(variant['Year'])+"</td>")
              #Topic
              fbrowse.write("<td>"+variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}']+"</td>")
              #Code avai
              fbrowse.write("<td>"+hasCode+"</td>")
              #Repl score
              rscore = variant['Replicate paper results score {0=NA, 1,2,3,4,5}']
              if ( rscore != ''):
                  if( rscore >= 4 ) :
                      step2dataYear[0] = step2dataYear[0] + 1
                  elif ( rscore > 1 ) :
                      step2dataYear[1] = step2dataYear[1] + 1
                  else :
                      step2dataYear[2] = step2dataYear[2] + 1
              fbrowse.write("<td>"+str(rscore)+"</td>")
              #Pseudocode only
              fbrowse.write("<td>"+ hasPseudoCode+"</td>")
              #Pseudo score
              pscore = variant['If pseudo-code, could the paper be trivially implemented? {0..4}']
              if ( pscore != ''):
                  if (not variant["If code not available, pseudo-code available (boolean)"]):
                       print( "[WARNING] Inconsistent choice for pseudo-code availability and score [ https://replicability.graphics/papers/" + doiclean+"/index.html  "+ variant['DOI'] + "]" )
                  if( pscore >= 4 ) :
                      step2dataYear[5] = step2dataYear[5] + 1
                  else :
                      step2dataYear[6] = step2dataYear[6] + 1
              fbrowse.write("<td>"+str(pscore)+"</td>")
              #Doc score
              fbrowse.write("<td>"+str(variant['Documentation score {0=NA,1,2,3}'])+"</td>")
              #altmetric
              if altmetric[0] != -1:
                  fbrowse.write('   <td> <a href="'+altmetric[2]+'"><img width="30px" src="'+str(altmetric[1])+'"></a><span style="font-size:0%">'+str(altmetric[0])+'</span></td>')
              else:
                  fbrowse.write("<td></td>")

              if ( variant["ACM Open Access (boolean)"]):
                  step2dataYearPdf[0] = step2dataYearPdf[0] +1
              if variant["PDF on the authors' webpage / institution (boolean)"]==False  and variant['PDF URL']=="" and variant['PDF on Arxiv or any openarchive initiatives (boolean)']==False:
                  step2dataYearPdf[2] = step2dataYearPdf[2] +1
              else:
                  step2dataYearPdf[1] = step2dataYearPdf[1] +1

              fbrowse.write("</tr>")
              cpt+=1

   # sort by years
   step2data["years"]   = OrderedDict(sorted(step2data["years"].items()))
   step2data["yearspdf"]   = OrderedDict(sorted(step2data["yearspdf"].items()))

   step2data["cpt"] = cpt
   step2data["cptHasCode"] = cptHasCode
   step2data["cptVariants"] = cptVariants

   write_browse_step2(fbrowse, step2data)
   write_index_step2(findex, step2data)

   print("Generating pages...")
   for paper in fulldata:
      generateAllPages(pathPages,paper)

   fbrowse.close()
   findex.close()
