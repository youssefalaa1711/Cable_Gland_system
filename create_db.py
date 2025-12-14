from database import Base, engine, SessionLocal
from models import Gland
import sqlite3


def create_database():
    # Reset SQLAlchemy tables for unarmoured
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ==========================
    # UNARMOURED GLANDS DATA
    # ==========================
    unarmoured_data = [
        (7, 11, "SA2-20S"),
        (10, 13.5, "SA2-20"),
        (12, 16.5, "SA2-25S"),
        (14.5, 19.5, "SA2-25"),
        (20.0, 25.0, "SA2-32S"),
        (21.5, 26.5, "SA2-32"),
        (23, 29, "SA2-40S"),
        (26.0, 31.5, "SA2-40"),
        (31.5, 37.5, "SA2-50S"),
        (36.0, 42.5, "SA2-50"),
        (42.0, 50.0, "SA2-63S"),
        (49.5, 55.0, "SA2-63"),
        (54.5, 61.0, "SA2-75S"),
        (60.5, 67.0, "SA2-75"),
    ]

    for min_s, max_s, gland in unarmoured_data:
        db.add(Gland(min_size=min_s, max_size=max_s, gland_size=gland))

    db.commit()
    db.close()

    # ==========================
    # ARMOURED GLANDS TABLE
    # ==========================
    conn = sqlite3.connect("cable_glands.db")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS armoured_glands")

    cur.execute("""
        CREATE TABLE armoured_glands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gland_type TEXT NOT NULL,        -- C1W, E1SW, C1X
            gland_size TEXT NOT NULL,        -- 20S, 20SS, 25S, etc.
            inner_min REAL,
            inner_max REAL,
            outer_min REAL NOT NULL,
            outer_max REAL NOT NULL
        )
    """)

    # ==========================
    # SAMPLE DATA (expand later)
    # ==========================

    armoured_data = [
        # C1W (outer only)
        ("C1X", "20SS", None, None, 6.1, 11.5),
        ("C1W", "20S", None, None, 9.5, 15.9),
        ("C1W", "20L", None, None, 12.5, 20.9),
        ("C1W", "25S", None, None, 14.0, 22.0),
        ("C1W", "25L", None, None, 18.2, 26.2),
        ("C1W", "32", None, None, 23.7, 33.9),
        ("C1W", "40", None, None, 27.9, 40.4),
        ("C1W", "50S", None, None, 35.2, 46.7),
        ("C1W", "50L", None, None, 40.4, 53.1),
        ("C1W", "63S", None, None, 45.6, 59.4),
        ("C1W", "63L", None, None, 54.6, 65.9),
        ("C1W", "75S", None, None, 59.0, 72.1),
        ("C1W", "75L", None, None, 66.7, 78.5),
        ("C1W", "90", None, None, 76.2, 90.4),
        ("C1W", "100", None, None, 89.1, 101.5),
        ("C1W", "115", None, None, 101.3, 110.3),
        ("C1W", "130", None, None, 114.0, 123.3),
        
        
        

        # E1SW (inner + outer — strict check)
        ("E1SW", "20SS", 3.1,  8.7,  6.1, 11.0),
        ("E1SW", "20S",  6.1, 11.7, 9.5, 15.9),
        ("E1SW", "20L",  6.5, 14.0, 12.5, 20.9),
        ("E1SW", "25S", 11.1, 20.0, 14, 22.0),
        ("E1SW", "25L", 11.1, 20.0, 18.2, 26.2),
        ("E1SW", "32", 17.0, 26.3, 23.7, 33.9),
        ("E1SW", "40", 22.0, 32.2, 27.9, 40.4),
        ("E1SW", "50S", 29.5, 38.2, 35.2, 46.7),
        ("E1SW", "50L", 35.6, 44.1, 40.4, 53.1),
        ("E1SW", "63S", 40.1, 50.0, 45.6, 59.4),
        ("E1SW", "63L", 47.2, 56.0, 54.6, 65.9),
        ("E1SW", "75S", 52.8, 62.0, 59.0, 72.1),
        ("E1SW", "75L", 59.1, 68.0, 66.7, 78.5),
        ("E1SW", "90",66.6, 79.4, 76.2,90.4),

        # C1X (outer only)
        ("C1X", "20SS", None, None, 6.1, 11.5),
        ("C1X", "20S", None, None, 9.5, 15.9),
        ("C1X", "20L", None, None, 12.5, 20.9),
        ("C1X", "25S", None, None, 14.0, 22.0),
        ("C1X", "25L", None, None, 18.2, 26.2),
        ("C1X", "32", None, None, 23.7, 33.9),
        ("C1X", "40", None, None, 27.9, 40.4),
        ("C1X", "50S", None, None, 35.2, 46.7),
        ("C1X", "50L", None, None, 40.4, 53.1),
        ("C1X", "63S", None, None, 45.6, 59.4),
        ("C1X", "63L", None, None, 54.6, 65.9),
        ("C1X", "75S", None, None, 59.0, 72.1),
        ("C1X", "75L", None, None, 66.7, 78.5),
        ("C1X", "90", None, None, 76.2, 90.4),
        ("C1X", "100", None, None, 89.1, 101.5),
        ("C1X", "115", None, None, 101.3, 110.3),
        ("C1X", "130", None, None, 114.0, 123.3),
        
        
    ]

    cur.executemany("""
        INSERT INTO armoured_glands
        (gland_type, gland_size, inner_min, inner_max, outer_min, outer_max)
        VALUES (?, ?, ?, ?, ?, ?)
    """, armoured_data)

    conn.commit()
    conn.close()

    print("Database created with full armoured range support!")


if __name__ == "__main__":
    create_database()
