!function($) {
  'use strict';

  const App = function() {
    this.dataId = ''
  };

  App.prototype.onDocReady = function(e) {
    const _this = $.App
    _this.dataId = $('#data-id').val()
    loumidisAPI.result.get(_this.dataId, function(err, res) {
      if (res) {
        if (res.output) {
          // $('#result-output').html(res.output.join('<br/>'))
        }
        if (res.errors) {
          $('#result-errors').html(res.errors.join('<br/>'))
        }
        if (res.step_2) {
          _this.renderTableStep2Count(res.step_2)
          _this.renderTableStep2GroupBy(res.step_2)
          _this.renderCountPieChart(res.step_2)
        }
        if (res.step_3) {
          if (res.step_3.images) {
            const html = res.step_3.images.map(
              image => `<img class="img-responsive pad" src="/images/${image}" alt="Photo">`
            )
            $('#result-images').html(html.join('<br/>'))
          }
        }
      }
    })
  },

  App.prototype.renderTableStep2Count = function(data) {
    const labels = ['UNDER', 'OVER', 'RIGHT']
    data.value_counts.map((item, index) => {
      const per = Math.round(item.norm * 100)
      $(`#step2-${index+1}0`).text(item.product_type)
      $(`#step2-${index+1}1`).text(item.count)
      $(`#step2-${index+1}2`).css('width', `${per}%`)
      $(`#step2-${index+1}3`).text(`${per}%`)
    })
  }

  App.prototype.renderTableStep2GroupBy = function(data) {
    const labels = ['UNDER', 'OVER', 'RIGHT']
    data.value_counts_group.map(item => {
      item.counts.map((count, index) => {
        const per = Math.round(count[2] * 100)
        const html = index
          ? `
            <tr>
              <td>${labels[count[0]]}</td>
              <td>${count[1]}</td>
              <td>
                <div class="progress progress-xs">
                  <div class="progress-bar progress-bar-red" style="width: ${per}%">
                  </div>
                </div>
              </td>
              <td><span class="badge bg-red" id="step2-33">${per}%</span></td>
            </tr>`
          : `
            <tr>
              <td rowspan="${item.counts.length}">
                ${item.product_name}
              </td>
              <td>${labels[count[0]]}</td>
              <td>${count[1]}</td>
              <td>
                <div class="progress progress-xs">
                  <div class="progress-bar progress-bar-red" style="width: ${per}%">
                  </div>
                </div>
              </td>
              <td><span class="badge bg-red" id="step2-33">${per}%</span></td>
            </tr>`
          $('#table-step2-group-by > tbody:last-child').append(html)
      })
    })
  }

  App.prototype.renderCountPieChart = function (data) {
    var colors = ['#f56954', '#00a65a', '#f39c12', '#00c0ef']
    var pieChartCanvas = $('#pie-chart-counts').get(0).getContext('2d')
    var pieChart       = new Chart(pieChartCanvas)
    var PieData        = data.value_counts.map(
      (item, index) => ({
        value    : item.count,
        color    : colors[index],
        highlight: colors[index],
        label    : item.product_type
      }))

    var pieOptions     = {
      //Boolean - Whether we should show a stroke on each segment
      segmentShowStroke    : true,
      //String - The colour of each segment stroke
      segmentStrokeColor   : '#fff',
      //Number - The width of each segment stroke
      segmentStrokeWidth   : 2,
      //Number - The percentage of the chart that we cut out of the middle
      percentageInnerCutout: 50, // This is 0 for Pie charts
      //Number - Amount of animation steps
      animationSteps       : 100,
      //String - Animation easing effect
      animationEasing      : 'easeOutBounce',
      //Boolean - Whether we animate the rotation of the Doughnut
      animateRotate        : true,
      //Boolean - Whether we animate scaling the Doughnut from the centre
      animateScale         : false,
      //Boolean - whether to make the chart responsive to window resizing
      responsive           : true,
      // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
      maintainAspectRatio  : true,
      //String - A legend template
      legendTemplate       : '<ul class="<%=name.toLowerCase()%>-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
    }
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    pieChart.Doughnut(PieData, pieOptions)
  }

  // initializing
  App.prototype.init = function() {
    const $this = this;

    $(document).ready($this.onDocReady);
  },

  $.App = new App, $.App.Constructor = App

}(window.jQuery),

function($) {
  "use strict";

  $.App.init();
}(window.jQuery);
