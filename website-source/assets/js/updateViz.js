var myChartTopics = new Chart(document.getElementById('myChartTopics'), {
  type: 'horizontalBar',
  data: {
    labels: ['C1',
             'C2',
             'C3',
             'Total (code available)',
             'Total (code not available)',
             'PC1',
             'PC2',
             'Total (only pseudo-code)'],
    datasets: [
      { // colormap is qualitative, colorblind safe
        // http://colorbrewer2.org/#type=qualitative&scheme=Set2&n=3
        label: '2014',
        backgroundColor: ['rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(102,194,165)', 'rgb(102,194,165)', 'rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(102,194,165)'],
        borderColor: 'rgb(102,194,165)',
        data: [0, 0, 0, 0, 0, 0,0 ]
      },
      {
        label: '2016',
        backgroundColor: ['rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,141,98)', 'rgb(252,141,98)', 'rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,141,98)'],
        borderColor: 'rgb(252,141,98)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        label: '2018',
        backgroundColor: ['rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(141,160,203)', 'rgb(141,160,203)', 'rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(187,199,233)'],
        borderColor: 'rgb(141,160,203)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
    ]
  },
  options: {
    title: {
        display: true,
        text: ''
      },
    scales: {
      xAxes: [{ stacked: true }],
      yAxes: [{
        stacked: true,
        ticks: {
          suggestedMin: 0,
          suggestedMax: 1
        }
      }]
    }
  }
});


var myChartPdf = new Chart(document.getElementById('myChartPdf'), {
  type: 'horizontalBar',
  data: {
    labels: ['ACM Open Access',
             'Preprint available',
             'PDF not available'],
    datasets: [
      { // colormap is qualitative, colorblind safe
        // http://colorbrewer2.org/#type=qualitative&scheme=Set2&n=3
        label: '2014',
        backgroundColor: 'rgb(102,194,165)',
        borderColor: 'rgb(102,194,165)',
        data: [0, 0, 0]
      },
      {
        label: '2016',
        backgroundColor: 'rgb(252,141,98)',
        borderColor: 'rgb(252,141,98)',
        data: [0, 0, 0]
      },
      {
        label: '2018',
        backgroundColor: 'rgb(141,160,203)',
        borderColor: 'rgb(141,160,203)',
        data: [0, 0, 0]
      },
    ]
  },
  options: {
    title: {
        display: true,
        text: ''
      },
    scales: {
      xAxes: [{ stacked: true }],
      yAxes: [{
        stacked: true,
        ticks: {
          suggestedMin: 0,
          suggestedMax: 1
        }
      }]
    }
  }
});

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
table.on('search.dt', updateChartFromData())
