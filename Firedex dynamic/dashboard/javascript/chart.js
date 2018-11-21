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
      labels: [1, 2, 3, 4, 5, 6],
      datasets: [{
        data: [10, 15, 5, 10, 15, 5],
        backgroundColor: [
          'rgba(234,237,243,1)'
        ],
        borderColor: [
          'black'
        ],
        borderWidth: 1,
        pointBackgroundColor: 'rgba(234,237,243,1)',
        lineTension: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
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

function drawChart(labels, data) {
  var context = document.getElementById("chart-bandwidth").getContext('2d');

  chart.data.labels = labels;
  chart.data.datasets[0].data = data;

  chart.update();
}
