from functools import wraps
from flask import jsonify, request, current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
	as Serializer, BadSignature, SignatureExpired
	)
from app.models.user import User

PREVILLEGES = {
    8:
    [
        "/partners",
        "/password",
    ]
}

# param : role_id, route_name


def get_previllege(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'token is missing'})
        else:
            token = request.headers['Authorization']
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            s.loads(token)
        except SignatureExpired:
            return jsonify({
                'message': 'token is expired',
                'expired': True
                })
        except BadSignature:
            return jsonify({
                'message': 'token is invalid',
                'invalid': True
                })
        user = User.verify_auth_token(token)
        path = request.path.replace('/init', '')
        role_id = user.role_id
        if (role_id != 1 and path != ''):
            accessible = (path in PREVILLEGES[role_id])
        else: 
            accessible = True
        kwargs['accessible'] = accessible
        return f(*args, **kwargs)
    return decorated



