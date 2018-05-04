from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Handle database errors
# db.session.rollback() ensures that the changes that triggered
# the error are rolled back and don't continue to interfere with
# the rest of the session
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500