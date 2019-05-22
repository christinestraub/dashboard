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
    this.prodcutName = ''

    //
    this.getProductNames()
  };

  App.prototype.getProductNames = function () {
    loumidisAPI.product.list('name', function(err, res) {
      if (err) {
        console.log(err)
        return
      }

      res.map(name =>
        $('#product-name')
          .append($(`<option value="${name}">${name}</option>`))
      )
    })
  }

  App.prototype.getProductTypes = function () {
    loumidisAPI.product.list('type', function(err, res) {
      if (err) {
        console.log(err)
        return
      }

      res.map(type =>
        $('#product-type')
          .append($(`<option value="${type}">${type}</option>`))
      )
    })
  }

  App.prototype.getRecords = function () {
    const params = {
      start_date: moment(this.startDate).format('YYYY-MM-DD'),
      end_date: moment(this.endDate).format('YYYY-MM-DD'),
      product_type: this.productType,
      product_name: this.productName,
    }

    loumidisAPI.table.list(params, function(err, res) {
      if (err) {
        console.log(err)
        return
      }

      if (res.length) {
        const productNames = []
        const data = res.map(item => {
          if (productNames.indexOf(item[4]) === -1) {
            productNames.push(item[4])
          }
          item.unshift('')
          return item
        })

        // redraw table
        $.App.table.clear();
        $.App.table.rows.add(data);
        $.App.table.draw();

        // update product name
        $('#product-name').empty()
        $('#product-name').append($(`<option value="ALL</option>`))
        productNames.map(name =>
          $('#product-name')
            .append($(`<option value="${name}">${name}</option>`))
        )
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
    const filter = {search: 'applied'}
    // if search is applied we will select these rows
    const count = this.table.rows(filter).data().length
    if (count > 0) {
      this.table.rows(filter).select()
    } else {
      this.table.rows().select()
    }
  }

  App.prototype.onDeselectAll = function(e) {
    this.table.rows().deselect()
  }

  App.prototype.onSubmit = function(e) {
    const _this = $.App
    const rows = _this.table.rows({selected: true}).data();
    const data = rows.map(row => {
      row.shift() // remove blank cell
      row.shift() // remove id
      return row
    })
    const options = {
      'start_date': _this.startDate,
      'end_date': _this.endDate,
      'product_type': _this.productType,
      'product_name': _this.productName,
    }
    _this.submitData('database.csv', data, options)
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

    // Product Type
    $('#product-type').change(function () {
      $.App.productType = $("#product-type option:selected").val()
      $.App.getRecords()
    })

    // Product Name
    $('#product-name').change(function () {
      $.App.productName = $("#product-name option:selected").val()
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

