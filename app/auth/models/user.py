from app.core import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    
    create_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime, onupdate=db.func.now())

    # relationships with user profile is one to one
    #    RELATIONSHIP profile
    #     TYPE: one-to-one
    #     TARGET: UserProfile
    #     OWNERSHIP: users domain
    profile = db.relationship(type='one-to-one', target='UserProfile', ownership='users domain')


    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'create_at': self.create_at,
            'last_login': self.last_login
        }
    
   
    @classmethod
    def jwt_identity(cls, user):
        return user.id
    
    def jwt_claims(self):
        return {
            'role': self.role,
            'email': self.email,
            'is_active': self.is_active
        }

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)    
    
    def update_last_login(self):
        from datetime import datetime
        self.last_login = datetime.utcnow()
        db.session.commit()

    def deactivate(self):
        self.is_active = False
        db.session.commit()

    def activate(self):
        self.is_active = True
        db.session.commit()

    def change_role(self, new_role):
        self.role = new_role
        db.session.commit()

    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()

    def update_username(self, new_username):
        self.username = new_username
        db.session.commit()

    def update_password(self, new_password):
        self.set_password(new_password)
        db.session.commit()
        
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'create_at': self.create_at.isoformat() if self.create_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }