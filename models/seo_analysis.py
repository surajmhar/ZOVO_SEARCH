from datetime import datetime, timezone

from database import db


class SEOAnalysis(db.Model):
    __tablename__ = "seo_analyses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    url = db.Column(
        db.String(500),
        nullable=False
    )

    overall_score = db.Column(
        db.Integer,
        nullable=False
    )

    performance_score = db.Column(
        db.Integer,
        nullable=False
    )

    on_page_score = db.Column(
        db.Integer,
        nullable=False
    )

    technical_score = db.Column(
        db.Integer,
        nullable=False
    )

    mobile_score = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<SEOAnalysis {self.url} - {self.overall_score}>"