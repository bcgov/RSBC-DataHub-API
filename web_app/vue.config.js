module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/roadside-forms/' : '/',
  runtimeCompiler: true,
  pwa: {
    workboxPluginMode: "InjectManifest",
    workboxOptions: {
      swSrc: "src/service-worker.js",
      importWorkboxFrom: 'local'
    }
  }
}