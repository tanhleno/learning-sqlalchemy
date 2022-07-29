from sqlalchemy import create_engine
from sqlalchemy import text


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        {"x": 2, "y": 2}
    )
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM some_table"))
    print(result.all())
