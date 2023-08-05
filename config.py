
DB_URL = "postgres://postgres:adjain@1mg@localhost:5432/api_table"
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL,
    },
    "apps": {
        "models": {
            "models": ["models.db"]
        }
    }
}
