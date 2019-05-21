!function($) {
  'use strict';

  const App = function() {
    // Data table
    this.table = $('#data-table').DataTable({
      searching: true,
      columnDefs: [{
        orderable: false,
        className: 'select-checkbox',
        targets: 0,
        data: null,
        defaultContent: '',
      }],
      select: {
        style: 'multi',
        selector: 'td:first-child'
      },
      order: [[ 1, 'asc' ]]
    })

    // Options
    this.startDate = moment().format('YYYY-MM-DD')
    this.endDate =moment().format('YYYY-MM-DD')
    this.prodcutType = ''
  };

  App.prototype.getRecords = function () {
    const params = {
      start_date: moment(this.startDate).format('YYYY-MM-DD'),
      end_date: moment(this.endDate).format('YYYY-MM-DD'),
      product_type: this.productType,
    }

    loumidisAPI.table.list(params, function(err, res) {
      if (err) {

      } else {
        $.App.table.clear();
        $.App.table.rows.add(res);
        $.App.table.draw();
      }
    })
  }

  App.prototype.onDocReady = function(e) {
    // Start date
    $('#start-date-picker')
      .datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
      })
      .on('changeDate', function(e) {
        $.App.startDate = moment(e.date).format('YYYY-MM-DD')
        $.App.getRecords()
      });

    // End date
    $('#end-date-picker')
      .datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
      })
      .on('changeDate', function(e) {
        $.App.endDate = moment(e.date).format('YYYY-MM-DD')
        $.App.getRecords()
      });

    $('#start-date-picker').val($.App.startDate)
    $('#end-date-picker').val($.App.endDate)

    //
    $('#product-type').change(function () {
      $.App.productType = $("#product-type option:selected").val()
      $.App.getRecords()
    })

    // get all records
    $.App.getRecords()
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

