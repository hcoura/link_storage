import psycopg2

class LinkStorage:

    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS jslinks (\
            id SERIAL PRIMARY KEY,\
            url TEXT NOT NULL CONSTRAINT name_unique UNIQUE,\
            tries INTEGER DEFAULT 0,\
            crawled BOOLEAN DEFAULT FALSE)")
        self.conn.commit()

    def new_link(self, url):
        try:
            self.cursor.execute("INSERT INTO jslinks(url) VALUES (%s)", (url,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def set_crawled(self, url):
        try:
            self.cursor.execute("UPDATE jslinks SET crawled=TRUE  WHERE url=%s", (url,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def get_links(self):
        self.cursor.execute("SELECT (url) FROM jslinks WHERE crawled = FALSE AND tries < 3")
        rows = self.cursor.fetchall()
        rows = [r[0] for r in rows]
        return rows

    def set_tried(self, url_list):
        try:
            self.cursor.execute("UPDATE jslinks SET tries = tries + 1  WHERE url IN %s", (tuple(url_list),))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def get_not_crawled_links(self):
        self.cursor.execute("SELECT * FROM jslinks WHERE crawled = FALSE AND tries >= 3")
        rows = self.cursor.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
