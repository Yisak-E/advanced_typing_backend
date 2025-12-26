from app.extensions import db
from datetime import datetime


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column( db.String(512), unique=True, nullable=False, index=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    expires_at = db.Column(db.DateTime, nullable=False)

    revoked = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship(
        "User",
        back_populates="refresh_tokens"
    )

    def __repr__(self):
        return f"<RefreshToken user_id={self.user_id} revoked={self.revoked}>"

    def is_valid(self):
        return not self.revoked and self.expires_at > datetime.utcnow()
