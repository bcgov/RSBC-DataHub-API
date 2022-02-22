const { InjectManifest } = require('workbox-webpack-plugin')

module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/roadside-forms/' : '/',
  configureWebpack: {
    plugins: [
      new InjectManifest({
        swSrc: './src/service-worker.js'
      })
    ]
  }
}