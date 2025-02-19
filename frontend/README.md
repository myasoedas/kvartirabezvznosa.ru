Ниже представлена подробная пошаговая инструкция по настройке Webpack и Babel для разработки фронтенда по методологии БЭМ, когда исходники будут находиться в папке **frontend/src/**. Инструкция включает настройку файла **.gitignore**, создание структуры папок и установку всех необходимых пакетов.

---

## Шаг 1. Настройка .gitignore в корневой директории проекта

1. **Откройте корневую директорию вашего проекта** (например, `kvartirabezvznosa.ru/`).
2. **Редактируйте (или создайте) файл `.gitignore`** в корневой директории и добавьте следующие строки для исключения ненужных файлов, в частности папки `frontend/node_modules/`:

   ```gitignore
   # Игнорировать зависимости npm для фронтенда
   frontend/node_modules/

   # Игнорировать файлы сборки (если они генерируются в static_dev или другой папке)
   blogicum_project/static_dev/

   # Игнорировать системные файлы и кеши
   .DS_Store
   Thumbs.db
   *.log
   .cache/
   ```

3. **Закоммитьте изменения**:
   ```bash
   git add .gitignore
   git commit -m "Настроен .gitignore: исключены frontend/node_modules и другие ненужные файлы"
   ```

---

## Шаг 2. Создание папки frontend и переход в нее

1. **Создайте папку `frontend`** в корневой директории проекта (если она еще не создана):
   ```bash
   mkdir frontend
   ```
2. **Перейдите в папку `frontend`**:
   ```bash
   cd frontend
   ```

---

## Шаг 3. Создание структуры папок для верстки по БЭМ

В папке **frontend** создайте следующую структуру директорий:

```bash
mkdir -p src/blocks
mkdir -p src/images
mkdir -p src/pages
mkdir -p src/scripts
mkdir -p src/vendor
```

После этого структура должна выглядеть примерно так:

```
frontend/
└── src/
    ├── blocks/      # Компоненты по БЭМ (каждый блок в своей папке)
    ├── images/      # Исходные изображения
    ├── pages/       # Страницы или шаблоны для конкретных страниц
    ├── scripts/     # Глобальные JavaScript-файлы (например, index.js — точка входа)
    └── vendor/      # Внешние библиотеки (если нужны)
```

---

## Шаг 4. Инициализация npm и установка зависимостей

1. **Инициализируйте npm**, если файл `package.json` ещё не создан:
   ```bash
   npm init -y
   ```
2. **Установите необходимые пакеты** для сборки фронтенда:
   ```bash
   npm install --save-dev webpack webpack-cli babel-loader @babel/core @babel/preset-env css-loader sass-loader sass style-loader mini-css-extract-plugin clean-webpack-plugin

   npm install --save-dev webpack-remove-empty-scripts
   ```

**Пояснения:**
- **webpack, webpack-cli** – основной сборщик.
- **babel-loader, @babel/core, @babel/preset-env** – для транспиляции современного JavaScript.
- **css-loader, sass-loader, sass, style-loader** – для обработки SCSS/CSS.
- **mini-css-extract-plugin** – для извлечения CSS в отдельный файл.
- **clean-webpack-plugin** – для очистки папки сборки перед каждой новой сборкой.

---

## Шаг 5. Настройка Babel

Создайте файл **babel.config.js** (или .babelrc) в папке **frontend**:
   
```js
module.exports = {
  presets: ['@babel/preset-env'],
};
```

Это позволит Babel транспилировать ваш современный JavaScript в совместимый с целевыми браузерами код.

---

## Шаг 6. Настройка Webpack

В папке **frontend** создайте файл **webpack.config.js** со следующим содержимым:

```javascript
const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const RemoveEmptyScriptsPlugin = require('webpack-remove-empty-scripts');

module.exports = (env, argv) => {
  const isProd = argv.mode === 'production';

  return {
    // Определяем точки входа: стили (SCSS), скрипты (JS), и favicon.
    entry: {
      main: path.resolve(__dirname, 'src', 'pages', 'main.scss'),
      app: path.resolve(__dirname, 'src', 'scripts', 'app.js'),
      favicon: path.resolve(__dirname, 'src', 'images', 'fav', 'favicon.ico'), // Теперь favicon тоже обрабатывается
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
        {
          // Обработка изображений, включая WEBP и favicon
          test: /\.(png|jpe?g|gif|svg|webp|ico)$/, // Добавлен WEBP
          type: 'asset/resource',
          generator: {
            filename: 'images/[name][ext]', // Все изображения + favicon хранятся в images/
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
    ],
    mode: isProd ? 'production' : 'development',
  };
};
```

**Пояснения:**
- **Entry**: Указываем, что основной SCSS-файл находится в `frontend/src/styles/main.scss` (если его еще нет, создайте папку `styles` внутри `src/` и разместите там `main.scss`), а точка входа для JS — `frontend/src/scripts/index.js`.
- **Output**: Файлы сборки будут помещаться в `blogicum_project/static_dev`.  
- **publicPath**: Указан для корректного формирования URL при подключении файлов в Django-шаблонах.
- **Loaders**: Обрабатывают SCSS, CSS, JS, шрифты и изображения.
- **Plugins**: `CleanWebpackPlugin` очищает папку сборки, а `MiniCssExtractPlugin` извлекает CSS в отдельный файл.

---

## Шаг 8. Подключение статических файлов в Django-шаблоне

В файле **blogicum_project/template/base.html** (или в другой соответствующей папке шаблонов) подключите сгенерированные файлы:

```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мой лендинг{% endblock %}</title>
    <!-- Подключаем минифицированный CSS -->
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
    {% block content %}
    <!-- Контент страницы -->
    {% endblock %}
    <!-- Подключаем минифицированный JS -->
    <script src="{% static 'js/app.js' %}"></script>
</body>
</html>
```

**Замечание:**  
Убедитесь, что имена файлов в шаблоне соответствуют тем, что генерирует Webpack (например, если используются хеши, возможно, потребуется обновлять шаблон вручную или использовать django-webpack-loader, но в данном случае вы подключаете файлы вручную).

---

## Шаг 9. Сборка и деплой

1. **Сборка фронтенда:**  
   Находясь в папке `kvartirabezvznosa.ru/frontend/`, выполните:
   ```bash
   npx webpack --mode production
   ```
   Это создаст минифицированные файлы в папке `blogicum_project/static_dev`.

2. **Сборка статики Django:**  
   Перейдите в папку `kvartirabezvznosa.ru/blogicum_project/` и выполните:
   ```bash
   python manage.py collectstatic --noinput
   ```
   Это скопирует файлы из `static_dev` в `static` (либо отправит их в S3, если настроено).

3. **Деплой проекта:**  
   Убедитесь, что ваш CI/CD процесс (например, GitHub Actions) запускает эти команды, чтобы обновления автоматически попадали на продакшен.

---

## Итоговый процесс

1. **Настройте .gitignore** в корневой директории, чтобы исключить `frontend/node_modules/` и другие временные файлы.
2. **Работайте в папке `frontend/`** для разработки исходного кода по БЭМ:
   - Исходники (SCSS, JS, блоки, изображения, шрифты) размещаются в `frontend/src/` (и её подкаталогах).
3. **Настройте Webpack и Babel** в папке `frontend/`:
   - Конфигурация Webpack (`webpack.config.js`) размещается в `frontend/` и использует исходники из `frontend/src/`.
   - Результат сборки (минифицированные файлы) сохраняется в `blogicum_project/static_dev/`.
4. **Настройте Django**:
   - Шаблоны (например, `base.html`) расположены в `blogicum_project/template/` и подключают статические файлы через `{% static %}`.
   - Файл `settings.py` настроен так, чтобы `STATICFILES_DIRS` указывал на `blogicum_project/static_dev`, а `STATIC_ROOT` – на `static/`.
5. **Запустите сборку**:  
   Из папки `frontend/` выполните `npx webpack --mode production`.
6. **Соберите статику Django**:  
   Перейдите в `blogicum_project/` и выполните `python manage.py collectstatic --noinput`.
7. **Автоматизация деплоя**:  
   Ваш CI/CD процесс запускает сборку и деплой, обновляя продакшен-среду.

Эта инструкция должна быть понятной и повторяемой, обеспечивая разделение исходного кода фронтенда в папке `frontend/` и финальной сборки в `blogicum_project/static_dev/`, с дальнейшей интеграцией в шаблоны Django. Если возникнут дополнительные вопросы или потребуется уточнение – пишите!

---

Добавим файл **normalize.css**. Его можно скачать с сайта: https://necolas.github.io/normalize.css/

Скопируйте содержимое файла normalize.css в браузере и вставьте в файл vendor/normalize.css. 

Подключите normalize.css в файле main.scss .

```scss
@use "../vendor/normalize.css" as *;
``` 

---

### Загрузка бесплатных шрифтов Inter

Перейдите на сайт: https://gwfh.mranftl.com/

В поиске напишите: Inter

Проставьте галки cyrillic latin

Выберите размер шрифтов для основного текста и заголовков 400 (regular), 700, 900

Cкачайте шрифты и поместите их в папку vendor/fonts/

Создайте файл vendor/fonts.scss и скопируйте в него код с сайта для подключения шрифтов.

```css
/* inter-regular - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  src: url('../fonts/inter-v18-cyrillic_latin-regular.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
/* inter-italic - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: italic;
  font-weight: 400;
  src: url('../fonts/inter-v18-cyrillic_latin-italic.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
/* inter-700 - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  src: url('../fonts/inter-v18-cyrillic_latin-700.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
/* inter-700italic - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: italic;
  font-weight: 700;
  src: url('../fonts/inter-v18-cyrillic_latin-700italic.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
/* inter-900 - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  src: url('../fonts/inter-v18-cyrillic_latin-900.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
/* inter-900italic - cyrillic_latin */
@font-face {
  font-display: swap; /* Check https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display for other options. */
  font-family: 'Inter';
  font-style: italic;
  font-weight: 900;
  src: url('../fonts/inter-v18-cyrillic_latin-900italic.woff2') format('woff2'); /* Chrome 36+, Opera 23+, Firefox 39+, Safari 12+, iOS 10+ */
}
  ```
Я отредактирвал исходный файл и добавил путь до шрифтов ../vendor/fonts/ вместо исходного ../fonts/ .

Создайте файл page/main.scss - в этот файл мы будем подключать все файлы стилей.

```scss
@use '../vendor/fonts.scss' as *;
```

Добавим в main.scss стили для заголовков и параграфов

```scss
@use '../../node_modules/normalize-scss/sass/normalize' as *;
@use '../vendor/fonts.scss' as *;

/* Базовые настройки */
body {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  background-color: #fff;
  margin: 0;
  padding: 0;
}

/* Заголовки */
h1, h2, h3, h4, h5 {
  font-family: 'Inter', sans-serif;
  font-weight: 900; // По умолчанию для заголовков самый жирный шрифт
  line-height: 1.2;
  margin: 0 0 16px;
}

h1 {
  font-size: 36px;
  font-weight: 900; // Самый жирный вариант
}

h2 {
  font-size: 30px;
  font-weight: 700;
}

h3 {
  font-size: 24px;
  font-weight: 700;
}

h4 {
  font-size: 20px;
  font-weight: 700;
}

h5 {
  font-size: 18px;
  font-weight: 700;
}

/* Параграфы */
p {
  font-size: 16px;
  font-weight: 400;
  margin-bottom: 16px;
  color: #444; // Чуть светлее основного текста
}

/* Курсивные заголовки */
h1 em,
h2 em,
h3 em,
h4 em,
h5 em {
  font-style: italic;
  font-weight: 700;
}

/* Курсивные параграфы */
p em {
  font-style: italic;
  font-weight: 400;
}
```

После каждого изменения в файле конфигурации webpack нужно очищать его кеш:

```bash
rm -rf node_modules/.cache
```

Команда запуска сборки webpack для продакшен:
```bash
npx webpack --mode production
```

Проверяем папку static_dev там должны быть все наши файлы и минифицированные файлы css и js.

Вносим правки в html шаблон base.html чтобы подключить стили и скрипты.

```html
<head>

<link rel="icon" href="{% static 'images/favicon.ico' %}" type="image/x-icon">
<link rel="stylesheet" href="{% static 'css/main.css'%}">
</head>
```

```html
<body class="root">

<script src="{% static 'js/app.js' %}"></script>
</body>

В папке blocks создадим файл root/root.scss:

```scss
.root {
  margin: 0;
  padding: 0;

  background: #2A2C2F;
}
```

