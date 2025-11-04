from app import app, db
from flask import request, jsonify
from model.user import User
from werkzeug.security import  check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required


@app.post("/login")
def login():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        if check_password_hash(user.password, password):
            access = create_access_token( identity=str(user.id),
                additional_claims={
                    "user_id": str(user.id),
                    "username": str(user.username)
                }
            )
            return jsonify(access_token=access)
        else:
            return jsonify({"msg": "Invalid username or password"}), 401





"""
@app.post('/auth/logout')
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()
    return jsonify({'msg': 'Successfully logged out'}), 200

"""

@app.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "user_id": user_id,
        "username": claims.get("username")
    })

