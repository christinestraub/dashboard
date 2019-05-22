!function($) {
  'use strict';

  const App = function() {
    // Data table
    this.table = $('#result-table').DataTable({
      searching: true,
      "columnDefs": [{
        "targets": -1,
        "data": null,
        "defaultContent": `
          <button class='btn btn-default btn-view'>Result</button>
          <button class='btn btn-default btn-run'>Data</button>
          <button class='btn btn-default btn-delete'>Delete</button>
         `
      }]
    })

    this.table.on('click', 'button.btn-view', function() {
      const data = $.App.table.row($(this).parents('tr')).data();
      window.location = `/result/${data[1]}`;
    });

    this.table.on('click', 'button.btn-run', function() {
      const data = $.App.table.row($(this).parents('tr')).data();
      window.location = `/result/${data[1]}`;
    });

    this.table.on('click', 'button.btn-delete', function() {
      const data = $.App.table.row($(this).parents('tr')).data();
      alert(data[0] +"'s salary is: "+ data[1]);
    });
  };

  App.prototype.onDocReady = function(e) {
    loumidisAPI.result.list(function(err, res) {
      if (res) {
        // redraw table
        const data = res.map(item => {
          item.push('')
          return item
        })

        $.App.table.clear();
        $.App.table.rows.add(data);
        $.App.table.draw();
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
