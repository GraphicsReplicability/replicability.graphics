import csv,os,sys, json,re,codecs
import hashlib
import shutil

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
    f.write("""<ul>""")
    f.write('<li><span class="family">Paper topic</span>: '+ variant['Topic {Rendering, Animation and Simulation, Geometry, Images, Virtual Reality, Fabrication}'] + '</li>\n')
    f.write('<li><span class="family">Software type</span>: '+ variant['Software type {Code, Binary, Partial Code}'] + '</li>\n')
    f.write('<li><span class="family">Able to run a replicability test</span>: '+ str(variant["Able to perform a replicability test (boolean)"]) + '</li>\n')
    f.write('<li><span class="family">Replicability score</span>: '+ str(variant['Replicate paper results score {0=NA, 1,2,3,4,5}']) + '</li>\n')

    f.write('<li><span class="family">License</span>: '+ variant["Code License (if any)"] + '</li>\n')
    f.write('<li><span class="family">Build mechanism</span>: '+ variant["Build/Configure mechanism"] + '</li>\n')
    f.write('<li><span class="family">Dependencies</span>: '+ variant["Dependencies"] + '</li>\n')
    f.write('<li><span class="family">Documentation score</span> {0,1,2}: '+ str(variant["Documentation score {0=NA,1,2,3}"]) + '</li>\n')
 #   f.write('<li><span class="family">Google Scholar Citation</span> ('+ row["Timestamp"] +'):   '+ str(row["Citation count (google scholar)"]) + '</li>\n')
    f.write('<li><span class="family">Reviewer</span>: '+ variant['Reviewer name'] + '</li>\n')

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

    ##switch psuedo
    f.write("We haven't found any source code from the authors.<br><br>")

    if not(variant['Code available (boolean)']) and variant['If code not available, pseudo-code available (boolean)']:
      f.write('<span class="family">Could paper be trivially implemented using the given pseudo-code? (1..5)</span>: '+ str(variant['If pseudo-code, could the paper be trivially implemented? {0..4}']) + '\n')
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

  if hasCode:
    if testRun:
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
        attribute = '<i class="fas fa-circle graphcol3"  style="font-size:150%;color:#bae4bc;" title="only pseudo-code available in the paper with simple implementation (score >=4)"></i>'
        signature[3] += 1

      else:
        attribute = '<i class="fas fa-circle graphcol4"  style="font-size:150%;color:#f0f9e8;" title="only pseudo-code available in the paper"></i>'
        signature[4] += 1

   ##PDF not available
  if hasOpenAccessPDF:
       attribute += ' <i class="fas fa-square graphcol5"  style="font-size:150%;color:#1b9e77;" title="PDF available as an ACM Open Access document"></i>'
       signature[5] += 1

  if row["PDF on the authors' webpage / institution (boolean)"]==False and row['PDF on Arxiv or any openarchive initiatives (boolean)']==False:
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


 if variant['Misc. comments'] != '':
    f.write("<br><br><br><h2>Misc. comments</h2>\n")
    f.write("<pre>" + re.sub('>','&gt;',re.sub('<','&lt;',variant['Misc. comments']))+"</pre>")
 else:
    f.write("\n")

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

 ##Export
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
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretty-checkbox@3.0/dist/pretty-checkbox.min.css">\n</head>\n<body>
  """)
 f.write('<ul class="publist-inline" style="text-align:left;"><li class="web"><a href="../../index.html">< Index</a></ul>')
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
    f.write("             <li><a href=\"#review-%d\">%s</a></li>\n" % (varid+1, var['Variant name']))
 f.write("             <li><a href=\"#review-%s\">&#43;</a></li>\n" % (len(paper)+1))
 f.write("</ul>")


 #and the remaining ones
 for varid, var in enumerate(paper):
    generatePage(f,pathPages,var,doi,doiclean,authors,varid+1)

 f.write('''<div id=review-%s>
            There are two options to add a review to this article:
            <ul><li>Open a pull request at <a href="https://github.com/GraphicsReplicability/replicability.graphics">https://github.com/GraphicsReplicability/replicability.graphics</a></li><li>Fill the form below (this option requires manual work and might be avoided if possible): <br>TODO: ADD FORM</li></ul>
            </div>
            '''% (len(paper)+1));

 f.write('</div></div>')


 #and the JS for the plot
 genChartFooter(f,paper)

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
 s.src = 'https://replicability-siggraph.disqus.com/embed.js';
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
  findex.write('<th>Citations (G.S.)</th>')
  findex.write('<th>Altmetric score</th>')
  findex.write('</tr></thead>\n<tbody>')

def dumpTableFooter(findex,topicsGlobal):
  findex.write('</tbody></table>')
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
            $(this).html('<select id="comboyear"><option value="">All Years</option><option value="2014">2014</option><option value="2016">2016</option><option value="2018">2018</option></select>');
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
    <li> <i class="fas fa-circle" style="font-size:150%;color:#bae4bc;" title="only pseudo-code available in the paper with simple implementation (score >=4)"></i> <b>(PC1)</b> only pseudo-code available in the paper with simple implementation (score >=4)
    <li> <i class="fas fa-circle" style="font-size:150%;color:#f0f9e8;" title="only pseudo-code available in the paper"></i> <b>(PC2)</b> only pseudo-code available in the paper
    <li> <i class="fas fa-square" style="font-size:150%;color:#1b9e77;" title="PDF available as an ACM Open Access document"></i> PDF available as an ACM Open Access document
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

def write_browse_step2(fbrowse, cpt, cptHasCode, cptVariants):
   dumpTableFooter(fbrowse,allTopics)

   fbrowse.write('''
            </div>
        </header>
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
def write_index_step2(findex, cpt, cptHasCode, cptVariants):
   findex.write('''
    <!-- First -->
    <section id="project" class="main">
      <header>
	<div class="container">
	  <h2>The Project</h2>
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
        for this field we compiled, ran and analyzed ''' + str(cptHasCode)+ ''' codes out of
       ''' + str(cpt) + ''' papers from 2014, 2016 and 2018 SIGGRAPH conferences. This
        analysis shows a clear increase in the number of papers with
        available and operational research codes with a dependency on
        the subfields, and indicates a correlation between code
        replicability and citation count.</p>

      <p style="text-align:left">This website provides an interactive tool to explore our results and evaluation data.
      It also provides tools to comment on the various codes either as an author or as a user. All materials (data, scripts..) that  have been used to generate these results are available on the  <a
      href="https://github.com/GraphicsReplicability/replicability.graphics"> <img width="20pt" src="images/github.png"/>&nbsp;replicability.graphics
      GitHub project</a>.</p>


     <p style="text-align:left"> Our project aims at providing the community with tools to improve Computer Graphics research replicability. Sharing this goal is the <a href="http://ReplicabilityStamp.org">Graphics
     Replicability Stamp Initiative</a> whose objective is to highlight replicable research works in Computer Graphics.</p>

      <p style="text-align:left">You can contribute new code analysis for computer graphics
      papers. We're looking forward to your <a href="#contribute" class="scrolly">contributions</a>. You can also <a href="#contact" class="scrolly">contact us</a>.</p>

    <!--<div class="row">
        <div class="column2 chart-container">
            <canvas height="150" id="myChartTopics" class="chartjs-render-monitor"></canvas>
        </div>
        <div class="column2 chart-container">
            <canvas height="150" id="myChartPdf" class="chartjs-render-monitor"></canvas>
        </div>
    </div>-->


	</div>
      </header>
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
		<p>Read our Siggraph 2020 paper on 374 analyzed Siggraph papers.</p>
	      </section>
	    </div>
	    <div class="col-4 col-12-narrow">
	      <section>
		<span class="feature-icon"><span class="icon solid fa-comments"></span></span>
		<header>
		  <h3><a href="#contribute" class="scrolly">Contribute</a></h3>
		</header>
		<p>Add comments or new analysis for Computer Graphics papers.</p>
	      </section>
	    </div>
	    <div class="col-12">
	      <footer>
		<a href="browse.html#data" class="button scrolly">''' + str(cptVariants) + ''' reviews so far</a>
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

                        <p>Main reference paper: <a href="">Nicolas Bonneel, David Coeurjolly, Julie Digne, Nicolas Mellado, <i>Code Replicability in Computer Graphics</i>, Siggraph 2020 </a></p>

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
                can either submit a proper JSON file as a <a
                href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request">pull request</a>
                to this <a href="https://github.com/GraphicsReplicability/replicability.graphics"><img width="20pt" src="images/github.png"/> project</a>, or send the JSON file to <a href=mailto:GraphicsReplicability@liris.cnrs.fr">GraphicsReplicability@liris.cnrs.fr</a>.</p>



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
	      <p>Drop us an email for more information or to let us know what you think.</p>
                </div>
	  <div class="content style4 featured">
	    <div class="container medium">
	      <form method="post" action="mailto:GraphicsReplicability@liris.cnrs.fr">
		<div class="row gtr-50">
		  <div class="col-6 col-12-mobile"><input type="text" placeholder="Name" /></div>
		  <div class="col-6 col-12-mobile"><input type="text" placeholder="Email" /></div>
		  <div class="col-12"><textarea name="message" placeholder="Message"></textarea></div>
		  <div class="col-12">
		    <ul class="actions special">
		      <li><input type="submit" class="button" value="Send Message" /></li>
		      <li><input type="reset" class="button alt" value="Clear Form" /></li>
		    </ul>
		  </div>
		</div>
	      </form>
	    </div>
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
   print("Generating index...")
   for paper in fulldata:
    for variant in paper:
      if isinstance(variant, str):
        print("Oops.. the variant is a string...")
      else:
        if isinstance(variant, list):
           print("Oops.. the variant is a list...")
        else:
           cptVariants += 1
           if variant['Is master variant (boolean)'] == True:

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
              else:
                hasCode = '×'

              hasPseudoCode = variant["If code not available, pseudo-code available (boolean)"]
              if hasPseudoCode==True:
                  hasPseudoCode = '✔️'
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
              fbrowse.write("<td>"+str(variant['Replicate paper results score {0=NA, 1,2,3,4,5}'])+"</td>")
              #Pseudocode only
              fbrowse.write("<td>"+ hasPseudoCode+"</td>")
              #Pseudo score
              fbrowse.write("<td>"+str(variant['If pseudo-code, could the paper be trivially implemented? {0..4}'])+"</td>")
              #Doc score
              fbrowse.write("<td>"+str(variant['Documentation score {0=NA,1,2,3}'])+"</td>")
              #GG
              fbrowse.write("<td></td>")
              #altmetric
              if altmetric[0] != -1:
                  fbrowse.write('   <td> <a href="'+altmetric[2]+'">'+str(altmetric[0])+'</a></td>')
              else:
                  fbrowse.write("<td></td>")

              fbrowse.write("</tr>")
              cpt+=1

   write_browse_step2(fbrowse, cpt, cptHasCode, cptVariants)
   write_index_step2(findex, cpt, cptHasCode, cptVariants)

   print("Generating pages...")
   for paper in fulldata:
      generateAllPages(pathPages,paper)

   fbrowse.close()
   findex.close()
