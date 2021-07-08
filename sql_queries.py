# DROP TABLES
users_table_drop = "DROP TABLE IF EXISTS users"
articles_table_drop = "DROP TABLE IF EXISTS articles"

# CREATE TABLES
users_table_create = ("""CREATE TABLE IF NOT EXISTS users(
    user_id TEXT PRIMARY KEY,
	user_name TEXT NOT NULL,
    link TEXT NOT NULL,
    description TEXT,
    followers INT
)""")

articles_table_create = ("""CREATE TABLE IF NOT EXISTS articles(
	title TEXT NOT NULL,
    link TEXT NOT NULL,
    user_id TEXT REFERENCES users(user_id),
    posting_time DATE NOT NULL,
    length_in_min INT NOT NULL,
    recommendations INT,
    responses INT
)""")

# INSERT RECORDS
users_table_insert = ("""INSERT INTO users VALUES (%s, %s, %s, %s, %s)
""")


# INSERT RECORDS
articles_table_insert = ("""INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s)
""")



# QUERY LISTS
create_table_queries = [users_table_create, articles_table_create]
drop_table_queries = [articles_table_drop, users_table_drop]
