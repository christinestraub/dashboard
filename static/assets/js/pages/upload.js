!function($) {
  'use strict';

  const App = function() {
    this.table = null
    this.file = null
  };


  App.prototype.initTable = function(e) {
    this.table = $('#example2').DataTable({
      searching: true
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
      $('.loader').show()
      loumidisAPI.data.submit(payload, function(err, res) {
        $('.loader').hide()
        if (err) {
          // show error modal
        } else {
          const id = res.id
          window.location = `/result/${id}`;
        }
      })
    }
  }

  App.prototype.clearOptions = function() {
    $('#start-date-picker').val('')
    $('#end-date-picker').val('')
    $("#product-type option:selected").val('OVER');
    $("#batch-size").text('10');
    $("#nominal-weight").text('100');
  }

  App.prototype.validateOptions = function() {
    const startDate = $('#start-date-picker').val()
    const endDate = $('#end-date-picker').val()
    const productType = $("#product-type option:selected").val()
    const batchSize = $('#batch-size').val()
    const nominalWeight = $('#nominal-weight').val()
    const options = {
      'start_date': startDate,
      'end_date': endDate,
      'product_type': productType,
      'batch_size': batchSize,
      'nominal_weight': nominalWeight
    }
    return options
  }

  App.prototype.onDocReady = function(e) {
    $.App.initTable()

    $("#upload").change(function() {
      if (this.files[0]) {
        const file = this.files[0];
        const config = {
          complete: function (results, file) {
            $('.loader').hide()

            if (results.errors.length) {
              // handle error
            }

            if (results.data[results.data.length - 1].length < 5) {
              results.data.pop();
            }

            results.data.shift();

            $.App.table.clear();
            $.App.table.rows.add(results.data);
            $.App.table.draw();
            $.App.file = file
          }
        };

        $('.loader').show()

        Papa.parse(file, config);
      }
    });

    $('#options-button').click(function(e) {
      e.preventDefault()
      const filter = { search: 'applied' }
      const data = $.App.table.rows(filter).data();
      // console.log(data.length)
      if (data.length > 0) {
        $('#modal-options').modal('show')
      } else {
        // $('#modal-info').modal('show')
        $('#modal-options').modal('show')
      }
    })

    $('#submit-button').click(function(e) {
      e.preventDefault()

      const options = $.App.validateOptions()
      const filter = { search: 'applied' }
      const data = $.App.table.rows(filter).data();
      const file = $.App.file

      $('#modal-options').modal('hide')
      $.App.submitData(file.name, data, options)
    })

    // Date picker
    $('#start-date-picker').datepicker({
      autoclose: true
    })
    $('#end-date-picker').datepicker({
      autoclose: true
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
