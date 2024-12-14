import mysql.connector
from models import Category, Equipment, Customer, Rental

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="rental_user",       
        password="Cpsy200d!",     
        database="rental_system_db"
    )
    return conn

def get_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Category(**row) for row in rows]

def add_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (category_id, name) VALUES (%s, %s)",
                       (category.category_id, category.name))
        conn.commit()
        return True, "Category added successfully."
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def get_equipment():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipment")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Equipment(**row) for row in rows]

def get_equipment_by_id(equipment_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipment WHERE equipment_id = %s", (equipment_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Equipment(**row) if row else None

def add_equipment(equipment):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO equipment (equipment_id, category_id, name, description, daily_rate, contact_phone, email, available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            equipment.equipment_id,
            equipment.category_id,
            equipment.name,
            equipment.description,
            equipment.daily_rate,
            equipment.contact_phone,
            equipment.email,
            equipment.available
        ))
        conn.commit()
        return True, "Equipment added successfully."
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def delete_equipment(equipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipment WHERE equipment_id = %s", (equipment_id,))
    conn.commit()
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()
    if rowcount > 0:
        return True, "Equipment deleted successfully."
    else:
        return False, "Equipment ID not found."

def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Customer(**row) for row in rows]

def add_customer(customer):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customers (customer_id, last_name, first_name, contact_phone, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            customer.customer_id,
            customer.last_name,
            customer.first_name,
            customer.contact_phone,
            customer.email
        ))
        conn.commit()
        return True, "Customer added successfully."
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()
    if rowcount > 0:
        return True, "Customer deleted successfully."
    else:
        return False, "Customer ID not found."

def get_rentals():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rentals")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    rental_list = []
    for row in rows:
        rental_obj = Rental(
            rental_id=row['rental_id'],
            date=row['rental_date'],
            customer_id=row['customer_id'],
            equipment_id=row['equipment_id'],
            return_date=row['return_date'],
            cost=row['cost']
        )
        rental_list.append(rental_obj)
    return rental_list

def add_rental(rental):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO rentals (rental_id, rental_date, customer_id, equipment_id, return_date, cost)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            rental.rental_id,
            rental.date,
            rental.customer_id,
            rental.equipment_id,
            rental.return_date,
            rental.cost
        ))

        cursor.execute("UPDATE equipment SET available = FALSE WHERE equipment_id = %s", (rental.equipment_id,))
        conn.commit()
        return True, "Rental added successfully."
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def generate_rental_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(rental_id) FROM rentals")
    max_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if max_id is None:
        return 1000
    else:
        return max_id + 1
