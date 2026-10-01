# import mysql.connector


# db = mysql.connector.connect(
#     host = "localhost",
#     user = "root" ,
#     password = "Prathvi9852@",
#     database = "pr1thviiii"
# )

# cursor = db.cursor()


from sqlalchemy import create_engine
from sqlalchemy import text
from urllib.parse import quote_plus
my_pass = "Prathvi9852@"
safe_password = quote_plus(my_pass)

our_URL = f"mysql+mysqlconnector://root:{safe_password}@localhost:3306/pr1thviiii"
engine = create_engine(our_URL,echo=True)

with engine.connect() as connection :
    result = connection.execute(text("SELECT 'Prithvi Connection Success!' AS msg"))
    a = result.fetchall()
    print(a)


