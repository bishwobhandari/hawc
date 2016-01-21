var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    devtool: 'cheap-module-eval-source-map',
    entry: [
        'webpack-hot-middleware/client?path=http://localhost:3000/__webpack_hmr',
        './assets/js/index'
    ],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: 'http://localhost:3000/dist/'
    },
    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
    ],
    module: {
        loaders: [{
            test: /\.js$/,
            loader: 'babel',
            include: path.join(__dirname, 'assets/js'),
            query: {
                plugins: [
                    ["react-transform", {
                        transforms: [{
                            transform: "react-transform-hmr",
                            imports: ["react"],
                            locals: ["module"]
                        }, {
                            "transform": "react-transform-catch-errors",
                            "imports": ["react", "redbox-react"]
                        }]
                    }]
                ]
            }
        }]
    }
};
