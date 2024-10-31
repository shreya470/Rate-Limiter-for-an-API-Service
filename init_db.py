from app import db, SocialMediaPost, app
from sqlalchemy import inspect
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')


# Initialize the database
with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")
    
    # Use inspector to list table names
    inspector = inspect(db.engine)
    print("Tables in the database:", inspector.get_table_names())
