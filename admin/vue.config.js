module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? process.env.PUBLIC_PATH
    : '/',
  configureWebpack: {
    devServer: {
      host: 'localhost',
      disableHostCheck: true,
    },
    devtool: 'source-map',
  },
};
