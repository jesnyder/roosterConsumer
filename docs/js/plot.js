

const dataPlot = {
  datasets: [{
    label: 'First Dataset',
    data: [{
      x: 20,
      y: 30,
      r: 15
    }, {
      x: 40,
      y: 10,
      r: 10
    }],
    backgroundColor: 'rgb(255, 99, 132)'
  }]
};


const config = {
  type: 'bubble',
  data: dataPlot,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Bubble Chart'
      }
    }
  },
};


new Chart(document.getElementById("dataPlot"), {
    "type": 'bubble',
    "data": dataPlot,
    "options": {
        "title": {
            "display": "true",
            "test": "Enrolled PDF"
        }
    }
});
