from app.extensions import db


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), unique=True, nullable=False)
    display_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    country = db.Column(db.String(100))
    profile_visibility = db.Column(db.Enum('public', 'private', 'friends-only', name='profile_visibility_enum'), default='public')  # e.g., public, private, friends-only
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user = db.relationship(type='one-to-one', target='User')
    
    def __repr__(self):
        return f'<UserProfile {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'display_name': self.display_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'country': self.country,
            'profile_visibility': self.profile_visibility,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def update_profile(cls, user_id, **kwargs):
        profile = cls.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = cls(user_id=user_id)
            db.session.add(profile)
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        db.session.commit()
        return profile