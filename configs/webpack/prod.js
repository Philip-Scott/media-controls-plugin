// production config
const { merge } = require("webpack-merge");
const { resolve } = require("path");

const commonConfig = require("./common");

module.exports = merge(commonConfig, {
  mode: "production",
  entry: "./index.tsx",
  output: {
    filename: "js/bundle.js",
    path: resolve(__dirname, "../../dist"),
    publicPath: "./dist",
  },
  devtool: "source-map",
  plugins: [],
});
