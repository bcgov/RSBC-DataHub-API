module.exports = {
  publicPath: process.env.VUE_APP_PUBLIC_PATH,
  runtimeCompiler: true,
  pwa: {
    workboxPluginMode: "InjectManifest",
    workboxOptions: {
      swSrc: "src/service-worker.js",
      importWorkboxFrom: 'local'
    }
  }
}