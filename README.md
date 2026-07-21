# Saucedemo Playwright Framework

Фреймворк автотестов для UI сайта [saucedemo.com](https://www.saucedemo.com), написанный на Python с использованием Playwright. Проект создан в рамках самостоятельного изучения UI-автоматизации, портфолио на позицию QA Automation Engineer.

## Стек технологий

- **Python 3.11**
- **Playwright** — управление браузером
- **pytest** / **pytest-playwright** — тестовый фреймворк и интеграция с Playwright
- **Allure** — отчётность
- **GitHub Actions** — CI/CD
- **python-dotenv** — управление переменными окружения

## Архитектура

Проект построен на паттерне **Page Object Model (POM)** — локаторы и действия с каждой страницей вынесены в отдельные классы, тесты работают через них, а не напрямую с `page.locator()`.

```
saucedemo-playwright-framework/
├── .github/
│   └── workflows/
│       └── tests.yml            # CI/CD конфигурация
├── pages/
│   ├── login_page.py            # авторизация
│   ├── inventory_page.py        # переход из каталога в корзину
│   ├── cart_page.py              # действия с товарами (каталог + корзина)
│   └── checkout_page.py         # оформление заказа
├── tests/
│   ├── test_login.py            # позитивные и негативные сценарии логина
│   ├── test_inventory.py        # каталог: отображение, сортировка, карточка товара
│   ├── test_cart.py              # корзина: добавление, удаление, состояние
│   └── test_checkout.py         # оформление заказа: форма, сумма, завершение
├── conftest.py                   # фикстуры подготовки состояния
├── config.py                     # чтение переменных окружения
├── pytest.ini
└── requirements.txt
```

## Что покрыто тестами

**Авторизация:**
- успешный вход
- заблокированный пользователь (`locked_out_user`)
- параметризованные негативные сценарии: неверный пароль, неверный логин, пустые поля, а также edge-cases — XSS, HTML-инъекция, SQL-инъекция, юникод, эмодзи, спецсимволы, экстремально длинная строка

**Каталог товаров:**
- отображение списка товаров
- сортировка по цене (по возрастанию/убыванию) и по имени (A-Z/Z-A) с проверкой порядка через сравнение с `sorted()`
- переход в карточку товара, проверка соответствия названия/цены/описания
- добавление/удаление товара прямо с каталога

**Корзина:**
- добавление и удаление товара с проверкой счётчика и содержимого
- повторное добавление после удаления (проверка корректности состояния)
- добавление нескольких товаров с проверкой названий, цен и описаний

**Оформление заказа:**
- переход к оформлению, проверка полей формы
- параметризованная проверка обязательных полей (First Name, Last Name, Zip Code)
- заполнение формы → проверка страницы Overview: соответствие товаров, расчёт Item total + Tax = Total
- завершение заказа (Finish), проверка сообщения об успехе
- скачивание PDF-чека заказа (`page.expect_download()`)

## Запуск тестов локально

```bash
git clone <repo-url>
cd saucedemo-playwright-framework
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
playwright install --with-deps chromium
```

Создать файл `.env` в корне проекта:
```
BASE_URL=https://www.saucedemo.com/
STANDARD_USER=standard_user
LOCKED_USER=locked_out_user
PASSWORD=secret_sauce
NAME=test_first_name
LAST_NAME=test_last_name
POSTAL_CODE=test_postal_code
```

Запустить тесты:
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## CI/CD

Тесты автоматически запускаются в GitHub Actions при каждом push и pull request в ветку `main`. Браузеры Playwright устанавливаются на раннере отдельным шагом (`playwright install --with-deps chromium`), тесты выполняются в headless-режиме. Результаты Allure сохраняются как артефакт прогона.

Учётные данные хранятся в GitHub Secrets, а не в коде.

## Автор

Михаил, [github.com/Mihail96tramontana](https://github.com/Mihail96tramontana)
