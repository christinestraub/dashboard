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
        const data = res.map(item => {
          item.unshift('')
          return item
        })
        $.App.table.clear();
        $.App.table.rows.add(data);
        $.App.table.draw();
      }
    })
  }

  App.prototype.submitData = function(filename, data, options) {
    if (data.length) {
      const aaa = []
      for (let i = 0; i < data.length; i++) {
        aaa.push(data[i]);
      };
      const payload = {
        filename,
        data: aaa,
        options
      }
      // console.log(payload)
      loumidisAPI.data.submit(payload, function(err, res) {
        if (err) {
          // show error modal
        } else {
          const id = res.id
          window.location = `/result/${id}`;
        }
      })
    }
  }

  App.prototype.onSelectAll = function(e) {
    this.table.rows().select()
  }

  App.prototype.onDeselectAll = function(e) {
    this.table.rows().deselect()
  }

  App.prototype.onSubmit = function(e) {
    const _this = $.App
    const rows = _this.table.rows({selected: true}).data();
    const data = rows.map(row => {
      row.shift()
      return row
    })
    const options = {
      'start_date': _this.startDate,
      'end_date': _this.endDate,
      'product_type': _this.productType,
    }
    _this.submitData('database', data, options)
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

