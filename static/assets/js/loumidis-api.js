const loumidisAPI = function ($) {
  const api = axios.create({
    baseURL: '/api'
  })

  api.interceptors.request.use(
    function(config) {
      return config
    },
    function(err) {
      return Promise.reject(err)
    }
  )

  api.interceptors.response.use(
    function(response) {
      return response
    },
    function(err) {
      return Promise.reject(err)
    }
  )

  const data = {
    get: function (data_id, callback) {
      api.get(`/data/${data_id}`)
        .then(function(res) {
          callback(null, res.data);
        })
        .catch(function(err) {
          callback(err)
        })
    },

    submit: function (data, callback) {
      api.post('/data/upload', data)
        .then(function(res) {
          callback(null, res.data);
        })
        .catch(function(err) {
          callback(err)
        })
    },
  }

  const table = {
    list: function (params, callback) {
      api.get('/table', { params })
        .then(function(res) {
          callback(null, res.data);
        })
        .catch(function(err) {
          callback(err);
        });
    },
  }

  //return an object that represents our new module
  return {
    data,
    table
  }

}(window.axios);

