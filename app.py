from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Тимчасова база
items = {}
next_id = 1

# Головна сторінка
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head><title>CRUD</title></head>
<body>
  <h1>Додати новий елемент</h1>
  <form method="POST" action="/create">
    Назва: <input type="text" name="name">
    <input type="submit" value="Додати">
  </form>

  <h2>Список:</h2>
  <ul>
    {% for id, name in items.items() %}
      <li>
        {{ id }}: {{ name }}
        <a href="/edit/{{ id }}">✏️</a>
        <form method="POST" action="/delete/{{ id }}" style="display:inline">
          <button type="submit">Видалити</button>
        </form>
      </li>
    {% endfor %}
  </ul>
</body>
</html>
'''

# Сторінка редагування
EDIT_TEMPLATE = '''
<!doctype html>
<html>
<head><title>Редагування</title></head>
<body>
  <h1>Редагувати елемент</h1>
  <form method="POST">
    Нова назва: <input type="text" name="name" value="{{ name }}">
    <input type="submit" value="Зберегти">
  </form>
  <a href="/">⬅️ Назад</a>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, items=items)

@app.route('/create', methods=['POST'])
def create():
    global next_id
    name = request.form['name']
    items[next_id] = name
    next_id += 1
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    items.pop(id, None)
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        items[id] = request.form['name']
        return redirect('/')
    name = items.get(id, '')
    return render_template_string(EDIT_TEMPLATE, name=name)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
