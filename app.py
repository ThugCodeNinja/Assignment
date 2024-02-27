import sqlite3
from flask import Flask, jsonify, request,g

app = Flask(__name__)

DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT, phone TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS companies
                 (id INTEGER PRIMARY KEY, name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER, company_id INTEGER, email TEXT, phone TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id),
                 FOREIGN KEY(company_id) REFERENCES companies(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS client_users
                 (id INTEGER PRIMARY KEY, client_id INTEGER, user_id INTEGER, 
                 created_at TEXT, updated_at TEXT, deleted_at TEXT, active INTEGER,
                 FOREIGN KEY(client_id) REFERENCES clients(id),
                 FOREIGN KEY(user_id) REFERENCES users(id))''')

conn.commit()

# Sample data
users = [
    {"id": 1, "username": "Rutam_Risaldar", "email": "abc@example.com", "phone": "1234567890"},
    {"id": 2, "username": "Rohit_Sharma", "email": "def@example.com", "phone": "9876543210"}
]

companies = [
    {"id": 1, "name": "ABC Magic Inc."},
    {"id": 2, "name": "XYZ TP Corp."},
    {"id": 3, "name": "Amazon"},
    {"id": 4, "name": "Jar"},
    {"id": 5, "name": "Google"}

]

clients = [
    {"id": 1, "name": "Client A", "user_id": 1, "company_id": 1, "email": "clientA@example.com", "phone": "1111111111"},
    {"id": 2, "name": "Client B", "user_id": 2, "company_id": 2, "email": "clientB@example.com", "phone": "2222222222"}
]

client_users = [
    {"id": 1, "client_id": 1, "user_id": 1, "created_at": "2023-02-28", "updated_at": "2023-02-28", "deleted_at": None, "active": 1},
    {"id": 2, "client_id": 2, "user_id": 2, "created_at": "2023-02-28", "updated_at": "2023-02-28", "deleted_at": None, "active": 1}
]

#2.1 Route to list app users
@app.route('/users', methods=['GET'])
def list_users():
    username = request.args.get('username')
    if username:
        filtered_users = [user for user in users if user['username'] == username]
        return jsonify(filtered_users)
    else:
        return jsonify(users)

#2.2 Route to replace some user fields at once
@app.route('/users/<int:user_id>', methods=['PUT','POST'])
def replace_user(user_id):
    data = request.json
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.update(data)

    return jsonify({'message': 'User updated successfully', 'user': user})

current_user = {
    'role': 'ROLE_ADMIN'
}

#2.3 Route to create some client
@app.route('/clients', methods=['POST'])
def create_client():
    if current_user.get('role') != 'ROLE_ADMIN':
        return jsonify({'message': 'Only ROLE_ADMIN users can create clients'}), 403
    data = request.json
    company_id = data.get('company_id')
    if not company_id:
        return jsonify({'message': 'Company ID is required'}), 400

    if next((client for client in clients if client['company_id'] == company_id), None):
        return jsonify({'message': 'Company already has a client'}), 400

    # Add new client to the list
    db = get_db()
    cursor = db.cursor()

    # Add new client to the list
    new_client = {
        'id': len(clients) + 1,
        'name': data.get('name'),
        'user_id': data.get('user_id'),
        'company_id': company_id,
        'email': data.get('email'),
        'phone': data.get('phone')
    }
    clients.append(new_client)
    
    # Inserting new client into the database
    cursor.execute('''INSERT INTO clients (name, user_id, company_id, email, phone)
                      VALUES (?, ?, ?, ?, ?)''', (new_client['name'], new_client['user_id'], new_client['company_id'],
                                                  new_client['email'], new_client['phone']))
    db.commit()

    return jsonify({'message': 'Client created successfully', 'client': new_client})


#2.4 Changing client fields

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.json
    client = next((client for client in clients if client['id'] == client_id), None)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    # Update client fields
    for key, value in data.items():
        if key in client:
            client[key] = value

    # Update client record in the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''UPDATE clients
                      SET name = ?, user_id = ?, company_id = ?, email = ?, phone = ?
                      WHERE id = ?''', (client['name'], client['user_id'], client['company_id'],
                                        client['email'], client['phone'], client_id))
    db.commit()

    return jsonify({'message': 'Client updated successfully', 'client': client})




'''
3. FUNCTIONS WITH SQL QUERIES

Fields like employee and revenue havent been added
'''

@app.route('/search/companies', methods=['GET'])
def search_companies():
    min_employees = request.args.get('min_emp')
    max_employees = request.args.get('max_emp')
    min_employees_int = int(min_employees) if min_employees else 0
    max_employees_int = int(max_employees) if max_employees else float('inf')
    db = get_db()
    cursor = db.cursor()

    query = '''
    SELECT * FROM companies
    WHERE employees >= ? AND employees <= ?;
    '''
    cursor.execute(query, (min_employees_int, max_employees_int))
    companies = cursor.fetchall()

    return jsonify({'companies': companies})

@app.route('/search/clients', methods=['GET'])
def search_clients():
    user_id = request.args.get('user_id')
    company_name = request.args.get('company_name')

    db = get_db()
    cursor = db.cursor()

    if user_id:
        query = '''
        SELECT * FROM clients
        WHERE user_id = ?;
        '''
        cursor.execute(query, (user_id,))
    elif company_name:
        query = '''
        SELECT * FROM clients
        JOIN companies ON clients.company_id = companies.id
        WHERE companies.name LIKE ?;
        '''
        cursor.execute(query, (f'%{company_name}%',))

    clients = cursor.fetchall()

    return jsonify({'clients': clients})

@app.route('/max_revenue/companies', methods=['GET'])
def max_revenue_companies():
    db = get_db()
    cursor = db.cursor()

    query = '''
    WITH max_revenue_by_industry AS (
        SELECT industry, MAX(revenue) AS max_revenue
        FROM companies
        GROUP BY industry
    )
    SELECT companies.id, companies.name, companies.industry, companies.revenue
    FROM companies
    JOIN max_revenue_by_industry as cte ON companies.industry = cte.industry
    WHERE companies.revenue = cte.max_revenue;
    '''
    cursor.execute(query)
    max_revenue_companies = cursor.fetchall()

    return jsonify({'max_revenue_companies': max_revenue_companies})

#5. Vaidation of incoming email
@app.route('/user/profile', methods=['GET'])
def user_profile():
    '''
    Getting user profile emails and validating them
    '''
    email = request.args.get('email')
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not email or not re.match(regex, email):
        return jsonify({'message': 'Invalid email format'}), 400

    return jsonify({'message': 'Email validated successfully', 'User Email': email})

 
if __name__ == '__main__':
    app.run(debug=True)
