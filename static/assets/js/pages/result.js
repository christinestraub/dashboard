!function($) {
  'use strict';

  const App = function() {
    this.dataId = ''
  };

  App.prototype.onDocReady = function(e) {
    this.dataId = $('#data-id').val()
    console.log('dataId', this.dataId)
    loumidisAPI.data.get(this.dataId, function(err, res) {
      if (res) {
        if (res.step_1) {
          $('#step_1_output').html(res.step_1.output.join('<br/>'))
        }
        if (res.step_2) {
          $('#step_2_output').html(res.step_2.output.join('<br/>'))
        }
        if (res.step_3) {
          $('#step_3_output').html(res.step_3.output.join('<br/>'))
        }
        if (res.step_4) {
          $('#step_2_output').html(res.step_4.output.join('<br/>'))
        }
        if (res.errors) {
          $('#errors_output').html(res.errors.join('<br/>'))
        }
      }
    })
  },

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
