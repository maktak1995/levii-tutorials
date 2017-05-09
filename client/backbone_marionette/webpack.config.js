var webpack = require('webpack');
var CleanPlugin = require('clean-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    entry:  './js/TodoMVC.js',
    output: {
        path:     __dirname + '/' + 'builds',
        filename: 'bundle.js',
        chunkFilename: '[name].bundle.js',
        publicPath: 'builds/'
    },
    plugins: [
       new ExtractTextPlugin('bundle.css'),
       new webpack.optimize.CommonsChunkPlugin({
           name:      'main',
           children:  true,
           minChunks: 2
       }),
       new webpack.ProvidePlugin({
         $: "jquery",
         jQuery: "jquery",
         "window.jQuery": "jquery"
       }),
    ],
    module: {
        rules: [
            {
              test:   /\.css/,
              use : ExtractTextPlugin.extract({ fallback: 'style-loader', use: 'css-loader'})
            },
            {
              test:   /\.html/,
              use : ['html-loader'],
            },
            {
              test:   /\.(png|gif|jpe?g|svg)$/i,
              use : ['url-loader'],
            },
        ],
    },
};
