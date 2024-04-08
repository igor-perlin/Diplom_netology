
# Админка - `/admin/`

Все функции доступны из админки и работают.
В проекте используется `SQLite3`

# Документация API  

## Регистрация

**URL**: `/register/`

**Method**: `POST`

**Body**:
```json
{
  "email": "user@example.com",
  "password": "yourpassword",
  "first_name": "First",
  "last_name": "Last",
  "user_type": "buyer"
}
```

## Генерация токена

**URL**: `/token/`

**Method**: `POST`

**Body**:
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

## Обновление токена

**URL**: `/token/refresh/`

**Method**: `POST`

**Body**:
```json
{
  "refresh": "<refresh_token>"
}
```

## Список товаторв

Получение списка всех товаров  
**Метод:** `GET`  
**URL:** `/products/`

## Фильтрация товаров
Для фильтрации товаров вы можете использовать различные параметры 
в URL.

### Фильтрация по категории
**Метод:** `GET`  
**URL:** `/products/?category=5`

Замените `5` на идентификатор интересующей вас категории. Этот запрос 
должен вернуть товары только из указанной категории.

### Фильтрация по цене
**Метод:** `GET`  
**URL:** `/products/?price_min=100&price_max=500`

Этот запрос фильтрует товары по цене, возвращая те, которые попадают 
в диапазон от 100 до 500. Адаптируйте значения price_min и price_max 
согласно вашим потребностям.

### Поиск товаров

**Метод:** `GET`  
**URL:**  `/products/?search=iphone`

Этот запрос ищет товары, содержащие слово "iphone" в любом из текстовых 
полей, указанных в search_fields вашего ProductViewSet. Измените "iphone" 
на любой другой поисковый запрос, который вы хотите проверить.

### Комбинированный запрос
Вы также можете комбинировать фильтры и поиск в одном запросе:

`**Метод:** `GET`  
**URL:**  `/products/?category=224&search=samsung`

Этот запрос будет искать товары, соответствующие поисковому запросу 
"samsung" в рамках категории с идентификатором 224.

## Корзина 

**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>` 

### Базовые эндпоинты для корзины:

* Добавление товара в корзину: `POST` `/cart/add/`
* Удаление товара из корзины: `POST` `/cart/remove/`. 
* Просмотр содержимого корзины: `GET` `/cart/`.

### Тестирование добавления товара в корзину

**Метод:** `POST`  
**URL:** `/cart/add/`

**Body** (raw JSON): 
```
{
  "product_id": "<product_id>",
  "quantity": "<quantity>"
} 
```

### Тестирование удаления товара из корзины

**Метод:** `POST`  
**URL:** `/cart/remove/`  

**Body** (raw JSON): 

``` 
{
  "product_id": "<product_id>"
}
```

### Тестирование просмотра содержимого корзины

**Метод:** `GET`  
**URL:** `/cart/`

### Получение списка всех контактов пользователя

**Метод:** `GET`  
**URL:** `/contacts/`

### Добавление нового контакта

**Метод:**  `POST`  
**URL:** `/contacts/`


**Body** (raw JSON): 
```
{
  "email": "example@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "phone": "+71234567890",
  "city": "Москва",
  "street": "Ленина",
  "house": "1",
  "building": "2",
  "structure": "",
  "apartment": "3"
}

```

### Удаление контакта
- Для удаления контакта, вам необходимо знать его ID. Предположим, 
что ID контакта, который вы хотите удалить, равен 1.

**Метод:** `DELETE`  
**URL:** `/contacts/1/`



### Обновление контакта

**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`   
-  Для обновления контакта также требуется его ID. Предположим, что вы
обновляете контакт с ID 1.
**Метод:**  `PUT` или `PATCH` для обновления  
**URL:** `/contacts/1/`  
**Метод:**  `PUT` или `PATCH` для обновления

**Body** (raw JSON):  
```
{
  "phone": "0987654321",
  "address": "321 Secondary St",
  "city": "AnotherCity",
}
```

## API запрос на подтверждение заказа

**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`   
**Метод:** `POST`  
**URL:** `/orders/{id}/confirm_order/`  

`{id}` Идентификатор заказа, который требуется подтвердить.

## Получение статуса и истории заказов пользователя

**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`  
**Метод:** `GET`  
**URL:** `/orders/`  

##  Восстановление пароля

**Метод:** POST  
**URL:** `/api/request_password_reset/`  
**Body** (raw JSON):  
``` 
{
    "email": "user@example.com"
}
```

`email:` Адрес электронной почты пользователя, зарегистрированного в системе.

## Сброс пароля

После получения письма с инструкциями пользователь должен выполнить POST-запрос 
на эндпоинт сброса пароля, передав токен и новый пароль:

**Метод:** `POST`  
**URL:** `/api/reset_password/{token}/`  
**Body** (raw JSON):  
```
{
    "new_password": "newStrongPassword"
}
```

## Обновление прайс-листа

**Метод**: POST  
**URL**: `/api/update_price/`  
**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`  
**Body** (raw JSON):  
```
{
  "shop": "Связной",
  "categories": [
    {"id": 224, "name": "Смартфоны"},
    {"id": 15, "name": "Аксессуары"}
  ],
  "goods": [
    {
      "id": 4216292,
      "category": 224,
      "model": "apple/iphone/xs-max",
      "name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
      "price": 110000,
      "price_rrc": 116990,
      "quantity": 14,
      "parameters": {
        "Диагональ (дюйм)": 6.5,
        "Разрешение (пикс)": 2688x1242
      }
    }
  ]
}
```

## Включение/отключение приёма заказов
**Метод:** `PATCH`  
**URL:** `/api/toggle_order_acceptance/`
**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`  
**Body** (raw JSON):  
```
{
  "is_accepting_orders": false
}
```
Ожидаемый результат: Состояние приёма заказов будет изменено на 
указанное в запросе, и вы получите подтверждение об успешном 
выполнении операции.

## Получение списка заказов
**Метод:** `GET`  
**URL:** `/api/orders/`  
**Headers**:  
- `Content-Type`: application/json
- `Authorization`: Bearer `<токен>`  

Ожидаемый результат: В ответе будут представлены все заказы, связанные 
с текущим пользователем (поставщиком), в формате JSON.