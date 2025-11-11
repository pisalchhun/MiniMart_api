from app import app, db
from flask import request, jsonify
from sqlalchemy import text
from model.user import User
from werkzeug.security import generate_password_hash



@app.get('/user/list')
def get_user():
    return get_all_user()

@app.get('/user/list/<int:user_id>')
def get_user_by_id(user_id):
    return get_all_by_id(user_id)


@app.post('/user/create')
def create_user():
    user = request.get_json()
    if not user:
        return {'message': 'no user data provided!'}
    if not user.get('username'):
        return {'message': 'username is required!'}
    if not user.get('email'):
        return {'message': 'email is required!'}
    if not user.get('password'):
        return {'message': 'password is required!'}

    username = user.get('username')
    email = user.get('email')
    password = user.get('password')

    user_obj = User(
        username= username,
        email= email,
        password=generate_password_hash(password)
    )
    db.session.add(user_obj)
    db.session.commit()

    last_id = user_obj.id
    #last_user = get_all_by_id(last_id)
    return {
        'status': 'create user success!',
       # 'user': last_user
    }


@app.put('/user/update')
def update_user():
    user = request.get_json()
    if not user:
        return jsonify({'message': 'No user data provided!'}), 400
    if not user.get('user_id'):
        return jsonify({'message': 'user id is required!'}), 400
    if not user.get('username'):
        return jsonify({'message': 'user name is required!'}), 400
    if not user.get('email'):
        return jsonify({'message': 'email is required!'}), 400

    user_id = user.get('user_id')
    username = user.get('username')
    email = user.get('email')

    user_obj = User.query.get(user_id)
    if not user_obj:
        return jsonify({'message': 'User not found!'}), 404
    user_obj.username = username
    user_obj.email = email
    db.session.commit()

    updated_user = get_all_by_id(user_id)
    return jsonify( {
        'status': 'update user success!'
    }), 200

@app.delete('/user/delete')
def delete_user():
    user = request.get_json()
    # assert False, user
    if not user.get('user_id'):
        return {'message': 'user_id is required!'}
    is_exists = get_all_by_id(user.get('user_id'))
    if is_exists.get('error'):
        return {'message': 'user not found!'}

    user_id = user.get('user_id')
    user_obj = User.query.get(user_id)
    db.session.delete(user_obj)
    db.session.commit()
    return {
        'status': 'delete user success!',
    }

def get_all_user():
    sql = text("SELECT id, username as name , email, password FROM user")
    result = db.session.execute(sql).fetchall()
    if not result:
        return {'message': 'no users found!'}
    rows = [dict(row._mapping) for row in result]
    return jsonify(rows)

def get_all_by_id(user_id: int):
    sql = text("SELECT id, username, email, password FROM user")
    result = db.session.execute(
        sql,
        {
            "user_id": user_id
        }
    ).fetchone()
    if not result:
        return {'error': 'user not found!'}
    row = dict(result._mapping)
    return row