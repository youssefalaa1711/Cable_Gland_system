from database import Base, engine, SessionLocal
from models import Gland
import sqlite3

def create_database():
    # Use SQLAlchemy to reset tables defined by models (keeps existing workflow for unarmoured)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    data = [
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

    for min_s, max_s, gland in data:
        db.add(Gland(min_size=min_s, max_size=max_s, gland_size=gland))

    db.commit()
    db.close()

    # Create armoured_glands table and insert sample data using sqlite3
    conn = sqlite3.connect("cable_glands.db")
    cur = conn.cursor()

    # Drop if exists to reset
    cur.execute("DROP TABLE IF EXISTS armoured_glands")

    # Create new table
    cur.execute("""
        CREATE TABLE armoured_glands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cable_type TEXT NOT NULL,
            min_size REAL NOT NULL,
            max_size REAL NOT NULL,
            gland_size TEXT NOT NULL
        )
    """)

    # Sample armoured data (adjust ranges as needed)
    armoured_data = [
        # SWA
        ("SWA", 8.0, 12.0, "SA2-20S"),
        ("SWA", 12.1, 15.5, "SA2-25S"),
        ("SWA", 15.6, 20.5, "SA2-32S"),
        ("SWA", 20.6, 30.0, "SA2-40"),
        # AWA
        ("AWA", 7.0, 11.0, "AW-20"),
        ("AWA", 11.1, 16.0, "AW-25"),
        ("AWA", 16.1, 26.0, "AW-32"),
        # STA
        ("STA", 6.5, 10.5, "ST-20"),
        ("STA", 10.6, 14.5, "ST-25"),
        ("STA", 14.6, 22.0, "ST-32"),
    ]

    cur.executemany(
        "INSERT INTO armoured_glands (cable_type, min_size, max_size, gland_size) VALUES (?, ?, ?, ?)",
        armoured_data
    )

    conn.commit()
    conn.close()

    print("Database created successfully with armoured_glands table!")

if __name__ == "__main__":
    create_database()
