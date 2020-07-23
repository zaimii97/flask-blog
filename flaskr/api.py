from .db import get_db
from flask import jsonify,Blueprint
bp= Blueprint("api",__name__,url_prefix="/api")

@bp.route("/posts",methods=("GET",))
def get_posts():
    db = get_db()
    posts=db.execute('SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY created DESC').fetchall()
    post_lists=[]
    counter=0
    for post in posts:
        post_lists.append(post)
        row = post_lists.pop(0)
        
    return row["title"]



















