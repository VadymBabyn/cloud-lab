from flask import Flask, request, jsonify

app = Flask(__name__)

# Уявна база даних (в оперативній пам'яті)
data = {}
id_counter = 1

@app.route('/')
def home():
    return 'Вітаю! Flask-додаток працює 🎉'

@app.route('/items', methods=['POST'])
def create_item():
    global id_counter
    item = request.json
    data[id_counter] = item
    id_counter += 1
    return jsonify({"id": id_counter - 1, "item": item}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def read_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id in data:
        data[item_id] = request.json
        return jsonify({"id": item_id, "updated": data[item_id]})
    return jsonify({"error": "Not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data:
        del data[item_id]
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
