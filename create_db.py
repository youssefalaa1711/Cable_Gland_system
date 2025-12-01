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
        ("C1W", "20S", None, None, 8.0, 12.0),
        ("C1W", "25S", None, None, 12.1, 15.5),
        ("C1W", "32S", None, None, 15.6, 20.5),

        # E1SW (inner + outer — strict check)
        ("E1SW", "20SS", 3.2,  8.5,  6.5, 13.0),
        ("E1SW", "20S",  6.0, 11.5, 10.0, 15.5),

        # C1X (outer only)
        ("C1X", "20S", None, None, 7.0, 11.0),
        ("C1X", "25S", None, None, 11.1, 16.0),
        ("C1X", "32S", None, None, 16.1, 26.0),
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
