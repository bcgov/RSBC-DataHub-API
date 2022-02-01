const { InjectManifest } = require('workbox-webpack-plugin')

module.exports = {
  publicPath: '/roadside-forms',
  configureWebpack: {
    plugins: [
      new InjectManifest({
        swSrc: './src/service-worker.js'
      })
    ]
  }
}