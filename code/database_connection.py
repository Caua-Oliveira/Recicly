import mysql.connector
import user as u


def connect_to_db():
    try:
        return mysql.connector.connect(
            host="sql10.freesqldatabase.com",  # Your public IP address
            user="sql10732886",
            password="GDgRUaCU1w",
            database="sql10732886"
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

def save_user_to_db(user):
    db = connect_to_db()
    if not db:
        return False
    cursor = db.cursor()

    sql = "INSERT INTO users (name, email, password, cpf, is_active) VALUES (%s, %s, %s, %s, %s)"
    values = (user.name, user.email, user.password.decode('utf-8'), user.cpf, user.is_active)
    try:
        cursor.execute(sql, values)
        db.commit()
    except Exception as e:
        print(f"Error saving user to database: {e}")
        return False
    cursor.close()
    db.close()
    return True

def fetch_user_by_email(email):
    db = connect_to_db()
    if not db:
        return None
    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result:
        user = u.User(
            name=result['name'],
            email=result['email'],
            password=result['password'].encode('utf-8'),
            cpf=result['cpf'],
            is_active=result['is_active']
        )
        return user
    return None

def update_user_in_db(user):
    db = connect_to_db()
    cursor = db.cursor()

    sql = "UPDATE users SET name = %s, email = %s, password = %s, is_active = %s WHERE cpf = %s"
    values = (user.name, user.email, user.password, user.is_active, user.cpf)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

def delete_user_from_db(cpf):
    db = connect_to_db()
    cursor = db.cursor()

    sql = "DELETE FROM users WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    db.commit()

    cursor.close()
    db.close()

def fetch_collection_location_by_login_id(login_id):
    return