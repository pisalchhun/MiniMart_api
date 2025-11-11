from app import app, db
from flask import request, jsonify
from model.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required, JWTManager


@app.post("/login")
def login():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        if check_password_hash(user.password, password):
            access = create_access_token( identity=str(user.id),
                additional_claims={
                    "msg":"login success",
                    "user_id": str(user.id),
                    "username": str(user.username),
                    "email": str(user.email)
                }
            )
            return jsonify(access_token=access)
        else:
            return jsonify({"msg": "Invalid username or password"}), 401


jwt = JWTManager(app)
jwt_blocklist = set()
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blocklist

# Logout route
@app.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200



@app.post("/reset-password")
@jwt_required()
def reset_password():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    old_password = str(data.get("old_password", "")).strip()
    new_password = str(data.get("new_password", "")).strip()
    if not old_password or not new_password:
        return jsonify({"msg": "Both old and new passwords are required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    if not check_password_hash(user.password, old_password):
        return jsonify({"msg": "Old password is incorrect"}), 400
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"msg": "Password updated successfully"}), 200

@app.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "user_id": user_id,
        "username": claims.get("username"),
        "email": claims.get("email")
    })

