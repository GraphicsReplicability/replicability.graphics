function myChartGenerateEmpty(idx){
    datasets = [
      // colormap is qualitative, colorblind safe
      // three first: http://colorbrewer2.org/#type=qualitative&scheme=Set2&n=3
      {
        backgroundColor: ['rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(102,194,165)', 'rgb(102,194,165)', 'rgb(179,221,210)', 'rgb(179,221,210)', 'rgb(102,194,165)'],
        borderColor: 'rgb(102,194,165)',
        data: [0, 0, 0, 0, 0, 0,0 ]
      },
      {
        backgroundColor: ['rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,141,98)', 'rgb(252,141,98)', 'rgb(252,184,168)', 'rgb(252,184,168)', 'rgb(252,141,98)'],
        borderColor: 'rgb(252,141,98)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        backgroundColor: ['rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(141,160,203)', 'rgb(141,160,203)', 'rgb(187,199,233)', 'rgb(187,199,233)', 'rgb(187,199,233)'],
        borderColor: 'rgb(141,160,203)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      // then https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=12
      {
        backgroundColor: ['rgb(254,203,146)', 'rgb(254,203,146)', 'rgb(254,203,146)', 'rgb(253,180,98)', 'rgb(253,180,98)', 'rgb(254,203,146)', 'rgb(254,203,146)', 'rgb(253,180,98)'],
        borderColor: 'rgb(253,180,98)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        backgroundColor: ['rgb(209,235,165)', 'rgb(209,235,165)', 'rgb(209,235,165)', 'rgb(179,222,105)', 'rgb(179,222,105)', 'rgb(209,235,165)', 'rgb(209,235,165)', 'rgb(179,222,105)'],
        borderColor: 'rgb(179,222,105)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        backgroundColor: ['rgb(252,205,229)', 'rgb(252,205,229)', 'rgb(252,205,229)', 'rgb(249,151,201)', 'rgb(249,151,201)', 'rgb(252,205,229)', 'rgb(252,205,229)', 'rgb(249,151,201)'],
        borderColor: 'rgb(249,151,201)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        backgroundColor: ['rgb(212,208,232)', 'rgb(212,208,232)', 'rgb(212,208,232)', 'rgb(190,186,218)', 'rgb(190,186,218)', 'rgb(212,208,232)', 'rgb(212,208,232)', 'rgb(190,186,218)'],
        borderColor: 'rgb(190,186,218)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },
      {
        backgroundColor: ['rgb(252,159,148)', 'rgb(252,159,148)', 'rgb(252,159,148)', 'rgb(251,128,114)', 'rgb(251,128,114)', 'rgb(252,159,148)', 'rgb(252,159,148)', 'rgb(251,128,114)'],
        borderColor: 'rgb(251,128,114)',
        data: [0, 0, 0, 0, 0, 0, 0]
      },

    ];
    return datasets[idx%datasets.length];
}


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
    datasets: []
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

function myChartPdfGenerateEmpty(idx){
    datasets = [
      { // colormap is qualitative, colorblind safe
        // http://colorbrewer2.org/#type=qualitative&scheme=Set2&n=3
        backgroundColor: 'rgb(179,221,210)',
        borderColor: 'rgb(102,194,165)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(252,184,168)',
        borderColor: 'rgb(252,141,98)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(187,199,233)',
        borderColor: 'rgb(141,160,203)',
        data: [0, 0, 0]
      },
      // then https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=12
      {
        backgroundColor: 'rgb(254,203,146)',
        borderColor: 'rgb(253,180,98)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(209,235,165)',
        borderColor: 'rgb(179,222,105)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(252,205,229)',
        borderColor: 'rgb(249,151,201)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(212,208,232)',
        borderColor: 'rgb(190,186,218)',
        data: [0, 0, 0]
      },
      {
        backgroundColor: 'rgb(252,159,148)',
        borderColor: 'rgb(251,128,114)',
        data: [0, 0, 0]
      },

    ];
    return datasets[idx%datasets.length];
}

var myChartPdf = new Chart(document.getElementById('myChartPdf'), {
  type: 'horizontalBar',
  data: {
    labels: ['ACM Open Access',
             'Preprint available',
             'PDF not available'],
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

