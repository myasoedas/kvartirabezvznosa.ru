const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const RemoveEmptyScriptsPlugin = require('webpack-remove-empty-scripts');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = (env, argv) => {
  const isProd = argv.mode === 'production';

  return {
    // Определяем точки входа: стили (SCSS), скрипты (JS), и favicon.
    entry: {
      main: path.resolve(__dirname, 'src', 'pages', 'main.scss'),
      app: path.resolve(__dirname, 'src', 'scripts', 'app.js'),
    },
    output: {
      // Собранные файлы будут помещаться в папку blogicum_project/static_dev
      path: path.resolve(__dirname, '..', 'blogicum_project', 'static_dev'),
      filename: isProd ? 'js/[name].js' : 'js/[name].js',
      // publicPath указывает, как файлы будут доступны в шаблонах Django
      publicPath: '/static/',
    },
    module: {
      rules: [
        {
          // Обработка SCSS/CSS файлов
          test: /\.s?css$/,
          use: [
            isProd ? MiniCssExtractPlugin.loader : 'style-loader',
            'css-loader',
            'sass-loader',
          ],
        },
        {
          // Обработка JS файлов через Babel
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
            },
          },
        },
        {
          // Обработка шрифтов
          test: /\.(woff(2)?|ttf|eot|otf)$/,
          type: 'asset/resource',
          generator: {
            filename: 'fonts/[name][ext]',
          },
        },
      ],
    },
    plugins: [
      new RemoveEmptyScriptsPlugin(), // Удаляет пустые JS-файлы, созданные для SCSS точки входа
      new CleanWebpackPlugin(),       // Очищает папку сборки перед каждой сборкой
      new MiniCssExtractPlugin({
        filename: isProd ? 'css/[name].css' : 'css/[name].css'
      }),
      // Копирование всех изображений из папки src/images в выходную папку images
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'src', 'images'),
            to: 'images',
          },
        ],
      }),
    ],
    mode: isProd ? 'production' : 'development',
  };
};
