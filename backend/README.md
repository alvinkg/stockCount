# VIRTUAL ENVIRONMENT

The virtual environment for this python app is using a directory 'react-flask-jwt' in the main folder REACT-FLASK-JWT

The command is: $ source react-flask-jwt/bin/activate

## Flask Migrate

## Install python-dotenv

alvinlim@coolhandsg-iMac backend % pip install python-dotenv

## Need to focus effort on SQLAlchemy ORM

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'

## for the dotenv variables

added a new file .env-localDO

