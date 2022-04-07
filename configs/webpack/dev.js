// development config
const { merge } = require("webpack-merge");
const commonConfig = require("./common");
const { resolve } = require("path");


module.exports = merge(commonConfig, {
  mode: "development",
  entry: [
      "./index.tsx", // the entry point of our app
  ],
  output: {
    filename: "js/bundle.js",
    path: resolve(__dirname, "../../dist"),
    publicPath: "./dist",
  },
  devtool: "cheap-module-source-map",
  plugins: [],
});
