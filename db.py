import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port = 3306,
  database='nekomata'
)

csr = db.cursor(prepared=True)
def get_name(user, password):
  sql = "SELECT * FROM user WHERE username=%s AND password=%s"
  csr.execute(sql, (user, password))
  resp = csr.fetchall()
  return resp



