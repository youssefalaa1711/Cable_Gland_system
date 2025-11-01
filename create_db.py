from database import Base, engine, SessionLocal
from models import Gland

def create_database():
    Base.metadata.drop_all(bind=engine)  # resets if you run again
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    data = [
        (7, 11, "20S"),
        (10, 13.5, "20"),
        (12, 16.5, "25S"),
        (14.5, 19.5, "25"),
        (20.0, 25.0, "32S"),
        (21.5, 26.5, "32"),
        (23, 29, "40S"),
        (26.0, 31.5, "40"),
        (31.5, 37.5, "50S"),
        (36.0, 42.5, "50"),
        (42.0, 50.0, "63S"),
        (49.5, 55.0, "63"),
        (54.5, 61.0, "75S"),
        (60.5, 67.0, "75"),
    ]

    for min_s, max_s, gland in data:
        db.add(Gland(min_size=min_s, max_size=max_s, gland_size=gland))

    db.commit()
    db.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
