module.exports = {
    chainWebpack: config => {
    config.module.rule('pdf')
      .test(/\.(pdf)(\?.*)?$/)
      .use('url-loader')
        .loader('url-loader')
        .options({
          name: 'assets/pdf/[name].[hash:8].[ext]'
        })

    },
    pwa: {
        workboxOptions: {
            skipWaiting: true
        }
    }
}