$(document).ready(function() {

  var context = document.getElementById("chart-bandwidth").getContext('2d');
  Chart.defaults.global.defaultFontColor = 'black';
  Chart.defaults.global.defaultFontFamily = 'Encode Sans Condensed';
  Chart.defaults.global.legend.display = false;
  Chart.defaults.global.tooltips.enabled = false;
  Chart.defaults.global.animation.duration = 0;

  var chart = new Chart(context, {
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
        yAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 1
          }
        }]
      }
    }
  });

});

function drawChart(labels, data) {
  var context = document.getElementById("chart-bandwidth").getContext('2d');

  var chart = new Chart(context, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: data,
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
        yAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 1
          }
        }]
      }
    }
  });

}
