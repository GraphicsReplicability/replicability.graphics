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

