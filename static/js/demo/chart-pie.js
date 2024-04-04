// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var backgroundColors = ['#4e73df', '#1cc88a', '#36b9cc', '#ff7f50', '#8a2be2', '#008080', '#ffa07a', '#bada55', '#800080', '#ffd700', '#00bfff', '#808000', '#6610f2', '#e83e8c', '#fd7e14', '#20c997'];
var hoverBackgroundColor = ['#2e59d9', '#17a673', '#2c9faf', '#e67e22', '#9400d3', '#008b8b', '#ff8c00', '#adff2f', '#ee82ee', '#ffff00', '#00ffff', '#008000', '#5a05f2', '#c7308c', '#f56914', '#1eb980'];

function selectBackgroundColors(num) {
  return backgroundColors.slice(0, num);
}

function selectHoverBackgroundColors(num) {
  return hoverBackgroundColor.slice(0, num);
}

function generatePieChart(chartId, labels, data) {
  var ctx = document.getElementById(chartId);
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: selectBackgroundColors(labels.length),
        hoverBackgroundColor: selectHoverBackgroundColors(labels.length),
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      responsive: true,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: true,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });
}