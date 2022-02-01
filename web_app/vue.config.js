const { InjectManifest } = require('workbox-webpack-plugin')

module.exports = {
  publicPath: './',
  configureWebpack: {
    plugins: [
      new InjectManifest({
        swSrc: './src/service-worker.js'
      })
    ]
  }
}