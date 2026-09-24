from flask import Flask, request, render_template_string, redirect
import sqlite3

app= Flask(__name__)

def init_db():
	conn = sqlite3.connect('users_db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS users
			(id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
	c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'supersecret123')")
	conn.commit()
	conn.close()
@app.route('/')
def home():
	return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
	message = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		conn = sqlite3.connect('users_db')
		c = conn.cursor()
		query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
		c.execute(query)
		user = c.fetchone()
		conn.close()
		if user:
			message = f'welcome, {username}!'
		else:
			message = 'Invalid credentials'
	return render_template_string('''
		<h2>Login</h2>
		<form method="post">
			username: <input name="username"><br>
			password: <input name="password" type="password"><br>
			<input type="submit">
		</form>
		<p>{{message}}</p>
		''', message=message)
@app.route('/search')
def search():
	query = request.args.get('q', '')
	return render_template_string('''
		<h2>Search</h2>
		<form method='get'>
			<input name='q' value='{{query}}'>
			<input type='submit'>
		</form>
		<p>You search for: ''' + query + '''</p>
	''', query=query)

if __name__ == "__main__":
	init_db()
	app.run(host='0.0.0.0', port=3000, debug=True)
