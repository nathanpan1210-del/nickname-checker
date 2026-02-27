from flask import Flask, jsonify, request
from db import load_data, add_person, search_by_name, delete_by_id

app = Flask(__name__)

@app.route('/api/names', methods=['GET'])
def get_all():
    """获取全部姓名"""
    return jsonify(load_data())

@app.route('/api/names', methods=['POST'])
def create():
    """添加姓名"""
    data = request.json
    new_person = add_person(data['name'])
    return jsonify(new_person), 201

@app.route('/api/names/search', methods=['GET'])
def search():
    """搜索姓名"""
    name = request.args.get('name', '')
    return jsonify(search_by_name(name))

@app.route('/api/names/<int:id>', methods=['DELETE'])
def remove(id):
    """删除姓名"""
    delete_by_id(id)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)