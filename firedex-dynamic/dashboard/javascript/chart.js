var chart;

$(document).ready(function() {

  var context = document.getElementById("chart-bandwidth").getContext('2d');
  Chart.defaults.global.defaultFontColor = 'black';
  Chart.defaults.global.defaultFontFamily = 'Encode Sans Condensed';
  Chart.defaults.global.legend.display = false;
  Chart.defaults.global.tooltips.enabled = false;
  Chart.defaults.global.animation.duration = 0;

  chart = new Chart(context, {
    type: 'line',
    data: {
      labels: [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      barValueSpacing: 20,
      scales: {
        xAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 5,
            autoSkip: true,
            maxTicksLimit: 15
          },
          scaleLabel: {
            display: true,
            labelString: "time (last 60 seconds)"
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 5
          },
          scaleLabel: {
            display: true,
            labelString: "messages received"
          }
        }]
      }
    }
  });

});

var allDatasets = [
  {
    label: "Blue",
    backgroundColor: "blue",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Red",
    backgroundColor: "red",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Green",
    backgroundColor: "green",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Yellow",
    backgroundColor: "yellow",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Orange",
    backgroundColor: "orange",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Purple",
    backgroundColor: "purple",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  },
  {
    label: "Brown",
    backgroundColor: "brown",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
    lineTension: 0,
    fill: false
  }
];

function drawChart(labels, currentDatasets) {
  var context = document.getElementById("chart-bandwidth").getContext('2d');

  var datasets = [];
  chart.data.datasets = datasets;

  for ( var i = 0; i < currentDatasets.length; i++ ) {
    var currentDataset = currentDatasets[i];
    allDatasets[i].data = currentDataset;
    chart.data.datasets[i] = allDatasets[i];
  }

  chart.update();
}
