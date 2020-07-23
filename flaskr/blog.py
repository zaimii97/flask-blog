from flask import Blueprint,render_template,redirect,request,flash,url_for,g,abort
from .db import get_db
from . auth import login_required

bp = Blueprint("blog",__name__)

@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        """SELECT post.id, title, body, created, author_id, username
         FROM post  JOIN user  ON post.author_id = user.id
         ORDER BY created DESC"""
    ).fetchall()
    return render_template("blog/index.html",posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')



def get_post(id,check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404,"post with the id {0} does not exist").format(id)

    if check_author and post["author_id"]!=g.user["id"]:
        abort(403)

    return post

@login_required
@bp.route("/<int:id>/update",methods=('GET' ,'POST'))
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?', (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))


    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))