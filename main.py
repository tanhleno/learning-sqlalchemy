from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey


metadata_obj = MetaData()
user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)
address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('id_user', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
metadata_obj.create_all(engine)

with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)"),
        [
            {"id": 1, "name": "Example", "fullname": "E-mail Example"},
            {"id": 2, "name": "Ciclano", "fullname": "Ciclano da Silva"}
        ]
    )
    conn.execute(
        text("INSERT INTO address (id, id_user, email_address) VALUES (:id, :id_user, :email)"),
        [
            {"id": 1, "id_user": 1, "email": "example@example.com"},
            {"id": 2, "id_user": 2, "email": "ciclanos@example.com"}
        ]
    )
    conn.commit()
with engine.connect() as conn:
    result = conn.execute(
        text(
            "SELECT fullname, email_address FROM user_account JOIN address " +
            "ON user_account.id == address.id_user"
        )
    )
    print()
    for row in result:
        print(f'Nome Completo: {row.fullname}')
        print(f'E-mail: {row.email_address}')
        print()
    conn.commit()
