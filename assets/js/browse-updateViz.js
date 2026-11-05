// Get the data from datatable
var table = $('#myTable').DataTable({
  order: [[ 7, "desc" ]],
  fixedHeader: true,
  paging: false,
  "columnDefs": [
{ "orderable": false, "targets": [0,1,2,3,4,5] }
]
});


function updateChartFromData() {
  var d = table.rows({
    filter: 'applied'
  }).data();
  var nb = 0;
  var colsYears  = []
  var colsTopics = [];
  var colsPdf    = [];
  // identifiers of the differents labels or rows of the chart
  var colNames = ["graphcol0",       // C1
                  "graphcol1",       // C2
                  "graphcol2",       // C3
                  "totalcode",       // computed: C1+C2+C3
                  "totalnocode",     // computed
                  "graphcol3",       // PC1
                  "graphcol4",       // PC2
                  "totalpseudocode", // computed: PC1+PC2
                  "graphcol5",       // ACM OA
                  "graphcol6",       // Preprint available
                  "graphcol7"];      // PDF not available
  var el = document.createElement( 'html' );
  totalperyear = [];

  // loop over entries selected in the table
  jQuery.each(d, function(index, value) {
    nb = nb + 1;
    el.innerHTML = value[2];

    year = value[4];


    // check if we found a new year
    yearidx = colsYears.indexOf( year );
    if (yearidx == -1) {
        yearidx = colsYears.length;
        colsYears.push(year);
        colsTopics.push([0, 0, 0, 0, 0, 0, 0, 0]);
        colsPdf.push([0, 0, 0]);
        totalperyear.push(0);
    }

    totalperyear[yearidx] ++;

    // loop over the graph columns (ie. the badges)
    jQuery.each(colNames, function(colIdx, colName) {
      // search if the current badge exists
      if(el.getElementsByClassName(colName).length != 0)
        // increment the correct entry for the graph
        if (colIdx <= 6){
          colsTopics[yearidx][colIdx] ++;
          if (colIdx <= 2) // compute total code
            colsTopics[yearidx][3] ++;
          else if (colIdx >= 5) // compute total pseudocode
            colsTopics[yearidx][7] ++;
        }
        else
          colsPdf[yearidx][colIdx-8] ++;
    } );
  });

  // compute no code
  var i;
  for (i = 0; i < totalperyear.length; i++) {
    colsTopics[i][4] = totalperyear[i] - colsTopics[i][3];
  }

  myChartTopics.options.title.text = ("Replicability (" + nb + " processed papers).");
  myChartPdf.options.title.text = ("Paper accessibility (" + nb + " processed papers).");


  //sort by year (assumes sortArrays.js has been included first)
  sorted = sortArrays([colsYears, colsTopics, colsPdf]);
  colsYears = sorted[0]
  colsTopics = sorted[1]
  colsPdf = sorted[2]

  // copy collected data in charts
  myChartTopics.data.datasets = [];
  myChartPdf.data.datasets = [];
  for(i = 0; i != colsYears.length; i++)
  {
    myChartTopics.data.datasets.push(myChartGenerateEmpty(i));
    myChartTopics.data.datasets[i].data  = colsTopics[i];
    myChartTopics.data.datasets[i].label = colsYears[i];

    myChartPdf.data.datasets.push(myChartPdfGenerateEmpty(i));
    myChartPdf.data.datasets[i].data  = colsPdf[i];
    myChartPdf.data.datasets[i].label = colsYears[i];
  }

  myChartTopics.update();
  myChartPdf.update();
}

// When the table is updated: update the chart
$(document).ready(function(){
  table.on('search.dt', updateChartFromData())
});
