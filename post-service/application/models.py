from . import db
from datetime import datetime


class Post(db.Model):
    ___table = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    msg_content = db.Column(db.Text, nullable=False)
    date_time_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_time_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.id}>'
    
class Comment(db.Model):
    ___table = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_time_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_time_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'
    

class Like(db.Model):
    ___table = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    like = db.Column(db.Boolean, nullable=False)
    date_time_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_time_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Like {self.id}>'
