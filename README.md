# Django Wallet API

REST API для управления кошельками и транзакциями, реализован на Django REST Framework с поддержкой JSON:API спецификации.

---

## 🔧 Стек
- Python 3.11+
- Django 4.2
- PostgreSQL
- Django REST Framework
- JSON:API
- Docker + docker-compose
- Pre-commit + black + isort + flake8 + pytest

---

## 🚀 Быстрый старт

### 📁 Клонировать репозиторий
```bash
git clone <YOUR_REPO>
cd django_wallet_api
```

### ⚙️ Запуск проекта
```bash
make up
```
Автоматически создаст `.env`, выполнит `docker compose down`, соберёт и поднимет контейнеры, применит миграции.


### 🧪 Тесты
```bash
make test
```

### 🧹 Линтинг и автоформат
```bash
make lint
```

### 🛑 Остановить проект
```bash
make down
```


---

## 🔗 Эндпоинты

### Wallets
```
GET    /api/wallets/
POST   /api/wallets/
GET    /api/wallets/<id>/
PATCH  /api/wallets/<id>/
DELETE /api/wallets/<id>/
```
Фильтрация:
```
GET /api/wallets/?filter[label]=Test
```

### Transactions
```
GET    /api/transactions/
POST   /api/transactions/
GET    /api/transactions/<id>/
PATCH  /api/transactions/<id>/
DELETE /api/transactions/<id>/
```
Фильтрация:
```
GET /api/transactions/?filter[wallet]=1&filter[amount_min]=50&filter[amount_max]=200
```

---

## 🧾 JSON:API

Требует `Content-Type: application/vnd.api+json`

Пример запроса создания транзакции:
```json
{
  "data": {
    "type": "transactions",
    "attributes": {
      "txid": "tx123456",
      "amount": "100.0"
    },
    "relationships": {
      "wallet": {
        "data": {"type": "wallets", "id": "1"}
      }
    }
  }
}
```

---

## 🧪 Pre-commit Hooks

Установка:
```bash
pre-commit install
```
Проверка вручную:
```bash
make lint
```

---

## 📁 Структура
```
apps/
  wallets/
    models.py
    views.py
    serializers.py
    services.py
    filters.py
    tests.py
```

---
