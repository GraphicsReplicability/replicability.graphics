// Get the data from datatable
var table = $('#myTable').DataTable({
  order: [[ 8, "des" ]],
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
  var colsTopics = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]];
  var colsPdf    = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]];
  var colNames = ["graphcol0",
                  "graphcol1",
                  "graphcol2",
                  "totalcode",
                  "totalnocode",
                  "graphcol3",
                  "graphcol4",
                  "totalpseudocode",
                  "graphcol5",
                  "graphcol6",
                  "graphcol7"];
  var el = document.createElement( 'html' );
  totalperyear = [0, 0, 0];

  // loop over entries selected in the table
  jQuery.each(d, function(index, value) {
    nb = nb + 1;
    el.innerHTML = value[2];

    year = value[4];
    yearidx = year == '2014' ? 0 : year == '2016' ? 1 : 2;
    totalperyear[yearidx] ++;

    // loop over the graph columns
    jQuery.each(colNames, function(colIdx, colName) {
      if(el.getElementsByClassName(colName).length != 0)
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
  myChartTopics.data.datasets[0].data = colsTopics[0];
  myChartTopics.data.datasets[1].data = colsTopics[1];
  myChartTopics.data.datasets[2].data = colsTopics[2];
  myChartPdf.data.datasets[0].data = colsPdf[0];
  myChartPdf.data.datasets[1].data = colsPdf[1];
  myChartPdf.data.datasets[2].data = colsPdf[2];

  myChartTopics.update();
  myChartPdf.update();
}

// When the table is updated: update the chart
$(document).ready(function(){
  table.on('search.dt', updateChartFromData())
});
