import psycopg2

class ContactManager:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            receiver_id INT REFERENCES contacts(id) ON DELETE CASCADE,
            message_text TEXT
        )
        """)
        self.connection.commit()

    def add_contact(self, name, phone, email):
        query = "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, phone, email))
        self.connection.commit()

    def get_contacts(self):
        self.cursor.execute("SELECT * FROM contacts ORDER BY id")
        rows = self.cursor.fetchall()
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]} | Email: {r[3]}")

    def send_message(self, receiver_id, message_text):
        query = "INSERT INTO messages (receiver_id, message_text) VALUES (%s, %s)"
        self.cursor.execute(query, (receiver_id, message_text))
        self.connection.commit()

    def view_messages(self):
        query = """
        SELECT m.id, c.name, c.phone, m.message_text
        FROM messages m
        JOIN contacts c ON m.receiver_id = c.id
        ORDER BY m.id DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if not rows:
            print("Hech qanday xabar yuborilmagan.")
        else:
            for msg in rows:
                print(f"ID: {msg[0]} | Kimga: {msg[1]} ({msg[2]})")
                print(f"Xabar: {msg[3]}")
                print("-" * 40)

    def close(self):
        self.cursor.close()
        self.connection.close()

def run_contact_manager():
    manager = ContactManager('n71_71', 'user71', '3103')
    while True:
        print("\n1. Kontakt qo'shish")
        print("2. Kontaktlarni ko‘rish")
        print("3. Xabar yuborish")
        print("4. Yuborilgan xabarlarni ko‘rish")
        print("0. Chiqish")
        choice = input("Tanlov: ")
        if choice == "1":
            name = input("Ism: ")
            phone = input("Telefon: ")
            email = input("Email: ")
            manager.add_contact(name, phone, email)
        elif choice == "2":
            manager.get_contacts()
        elif choice == "3":
            manager.get_contacts()
            receiver = input("Kontakt ID: ")
            text = input("Xabar matni: ")
            manager.send_message(receiver, text)
        elif choice == "4":
            manager.view_messages()
        elif choice == "0":
            manager.close()
            break
        else:
            print("Noto‘g‘ri tanlov!")

# run_contact_manager()
