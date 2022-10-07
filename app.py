from common import db, db_url, db_meta, TEST_USERNAME, TEST_PASSWORD
from main import app, socketio

if db_url == "sqlite:///app.db":
    db_meta.drop_all()
    db_meta.create_all()

if db_url == "sqlite:///test.db":
    db_meta.create_all()


def init_users():
    from common.users_db import User

    if User.find_by_username(TEST_USERNAME) is None:
        User.create(TEST_USERNAME, TEST_PASSWORD)


@app.after_request
def hey(res):
    db.session.commit()
    return res


with app.app_context():
    init_users()

if __name__ == "__main__":  # test only
    socketio.run(app=app, debug=True)
