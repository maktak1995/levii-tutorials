var webpack = require('webpack');
var CleanPlugin = require('clean-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var production = process.env.NODE_ENV === 'production';

module.exports = {
    entry:  './src',
    output: {
        path:     __dirname + '/' + 'builds',
        filename: 'bundle.js',
        chunkFilename: '[name].bundle.js',
        publicPath: 'builds/'
    },
    plugins: [
       new ExtractTextPlugin('bundle.css'), // <=== コンテンツがパイプされるべき場所 (エントリポイントで指定されるCSSだけが対象)
       new webpack.optimize.CommonsChunkPlugin({
           name:      'main', // 依存性を主(main)ファイルに移す
           children:  true,   // 全ての子に対しても共通する依存性を探す
           minChunks: 2       // この回数、依存性に遭遇したら抜き出す
       }),
    ],
    module: {
        loaders: [
            {
              test:   /\.js/,
              loader: 'babel-loader',
              include: __dirname + '/src'
            },
            {
              test:   /\.scss/,
              loader: ExtractTextPlugin.extract({ fallback: 'style-loader', use: ['css-loader','sass-loader']})
            },
            {
              test:   /\.html/,
              loader: 'html-loader'
            },
            {
              test:   /\.(png|gif|jpe?g|svg)$/i,
              loader: 'url-loader',
              query: {
                limit: 10000,
              },
            },
        ],
    },
};
