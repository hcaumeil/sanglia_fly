import psycopg2
from utils import expect_env_var

pg_db = expect_env_var("POSTGRESQL_ADDON_DB")
pg_host = expect_env_var("POSTGRESQL_ADDON_HOST")
pg_password = expect_env_var("POSTGRESQL_ADDON_PASSWORD")
pg_port = expect_env_var("POSTGRESQL_ADDON_PORT")
pg_user = expect_env_var("POSTGRESQL_ADDON_USER")

db = psycopg2.connect(
    dbname=pg_db, host=pg_host, password=pg_password, port=pg_port, user=pg_user
)
