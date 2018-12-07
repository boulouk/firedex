var chart;

$(document).ready(function() {

  var context = document.getElementById("chart-bandwidth").getContext('2d');
  Chart.defaults.global.defaultFontColor = 'black';
  Chart.defaults.global.defaultFontFamily = 'Encode Sans Condensed';
  Chart.defaults.global.legend.display = false;
  Chart.defaults.global.tooltips.enabled = false;
  Chart.defaults.global.animation.duration = 0;

  chart = new Chart(context, {
    type: 'bar',
    data: {
      labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
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
            stepSize: 1
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 5
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
  },
  {
    label: "Red",
    backgroundColor: "red",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
  },
  {
    label: "Green",
    backgroundColor: "green",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
  },
  {
    label: "Yellow",
    backgroundColor: "yellow",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
  },
  {
    label: "Orange",
    backgroundColor: "orange",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
  },
  {
    label: "Purple",
    backgroundColor: "purple",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
  },
  {
    label: "Brown",
    backgroundColor: "brown",
    data: [],
    borderColor: [
      'black'
    ],
    borderWidth: 1,
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
