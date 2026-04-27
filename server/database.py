# Contains the CRUD functions that connect the request to ../database.db where it can query and such.

# SHEMA
# CREATE TABLE parks (
# park_id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT NOT NULL,
# owned_by TEXT NOT NULL,
# year_opened INTEGER NOT NULL,
# visitors_per_year INTEGER NOT NULL,
# visitors_per_day INTEGER NOT NULL,
# location TEXT NOT NULL
# );

# CREATE TABLE sqlite_sequence(name,seq);
# CREATE TABLE manufacturers (
# manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT NOT NULL,
# year_founded INTEGER NOT NULL
# );

# CREATE TABLE rollercoasters (
# rollercoaster_id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT NOT NULL,
# type TEXT NOT NULL,
# model TEXT NOT NULL,
# manufacturer_id INTEGER NOT NULL,
# height TEXT NOT NULL,
# speed TEXT NOT NULL,
# length TEXT NOT NULL,
# year_opened INTEGER NOT NULL,
# year_closed INTEGER,
# currently_operating INTEGER,
# SBNO INTEGER,
# removed INTEGER,
# park_id INTEGER NOT NULL,
# riders_per_hour INTEGER,
# thrill_level TEXT NOT NULL,
# inversions INTEGER NOT NULL,
# avg_wait_time TEXT,
# height_restriction TEXT NOT NULL,
# ride_duration TEXT NOT NULL,
# lift_or_launch TEXT NOT NULL,
# cost INTEGER,
# drop_angle_in_degrees INTEGER,
# replaced_by_id INTEGER,
# age INTEGER NOT NULL,
# image TEXT,
# FOREIGN KEY (park_id) REFERENCES parks (park_id),
# FOREIGN KEY (manufacturer_id) REFERENCES manufacturers (manufacturer_id)
# );


import os
import sqlite3

class DB:
    """Lightweight SQLite helper for the app.

    Methods:
    - get_all_coasters() -> list[dict]
    - get_coaster_by_id(id) -> dict | None
    """
    def __init__(self, db_path: str = None):
        # Default to the database.db file at the repository root
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'database.db')
            )

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _row_to_dict(self, row: sqlite3.Row) -> dict:
        return {k: row[k] for k in row.keys()} if row is not None else None

    def _normalize(self, d: dict) -> dict:
        # Convert common tinyint flags to booleans for the frontend
        for flag in ('currently_operating', 'SBNO', 'removed'):
            if flag in d and d[flag] is not None:
                try:
                    d[flag] = bool(int(d[flag]))
                except Exception:
                    d[flag] = d[flag]
        return d

    def get_all_coasters(self):
        """Return a list of rollercoaster dicts with park and manufacturer names when available."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT rc.*, p.name AS park_name, m.name AS manufacturer_name
            FROM rollercoasters rc
            LEFT JOIN parks p ON rc.park_id = p.park_id
            LEFT JOIN manufacturers m ON rc.manufacturer_id = m.manufacturer_id
            ORDER BY rc.name COLLATE NOCASE
            """
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result

    def get_coaster_by_id(self, coaster_id: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT rc.*, p.name AS park_name, m.name AS manufacturer_name
            FROM rollercoasters rc
            LEFT JOIN parks p ON rc.park_id = p.park_id
            LEFT JOIN manufacturers m ON rc.manufacturer_id = m.manufacturer_id
            WHERE rc.rollercoaster_id = ?
            """,
            (coaster_id,)
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        d = self._row_to_dict(row)
        return self._normalize(d)
    
    def get_all_parks(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
             SELECT name, owned_by, year_opened, visitors_per_year, visitors_per_day, location, image
             FROM parks
            """
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_park_by_id(self, park_id: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name, owned_by, year_opened, visitors_per_year, visitors_per_day, location, image
            FROM parks
            WHERE park_id = ?
            """,
            (park_id,)
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        d = self._row_to_dict(row)
        return self._normalize(d)
    
    def get_all_manufacturers(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
             SELECT name, year_founded
             FROM manufacturers
            """
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_manufacturer_by_id(self, manufacturer_id: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name, year_founded
            FROM manufacturers
            WHERE manufacturer_id = ?
            """,
            (manufacturer_id,)
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        d = self._row_to_dict(row)
        return self._normalize(d)
    
    def get_coasters_by_park(self, park_name: str):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT rc.name AS rollercoaster
            FROM rollercoasters rc
            JOIN parks p ON p.park_id = rc.park_id
            WHERE p.name = ?
            """,
            (park_name,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_coasters_by_manufacturer(self, manufacturer_id: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT rc.name AS rollercoaster, p.name AS park
            FROM rollercoasters rc
            JOIN manufacturers m ON m.manufacturer_id = rc.manufacturer_id
            JOIN parks p ON p.park_id = rc.park_id
            WHERE m.manufacturer_id = ?
            """,
            (manufacturer_id,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_all_operating_coasters(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name
            FROM rollercoasters
            WHERE currently_operating = 1
            """,
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_all_defunct_coasters(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name
            FROM rollercoasters
            WHERE removed = 1
            """,
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_all_SBNO_coasters(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name
            FROM rollercoasters
            WHERE SBNO = 1
            """,
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        return result
    
    def get_coasters_above_height(self, height: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name, height
            FROM rollercoasters
            WHERE height > ?
            ORDER BY height
            """,
            (height,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        print(result)
        return result
    
    def get_coasters_below_height(self, height: int):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name, height
            FROM rollercoasters
            WHERE height < ? AND height > 0
            ORDER BY height;
            """,
            (height,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        print(result)
        return result
    
    def get_manufacturers_ranked_by_avg_height(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT m.name AS manufacturer, ROUND(AVG(rc.height), 2) AS avg_height
            FROM rollercoasters rc
            JOIN manufacturers m ON m.manufacturer_id = rc.manufacturer_id
            GROUP BY manufacturer
            ORDER BY avg_height DESC
            """,
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = self._row_to_dict(r)
            result.append(self._normalize(d))
        conn.close()
        print(result)
        return result
    
    
# Just for testing queries
# 1. Create an instance of your DB class
my_database = DB() 

# 2. Call the method on the instance!
results = my_database.get_manufacturers_ranked_by_avg_height()

# Optional: Print the results to see what you got
print(results)