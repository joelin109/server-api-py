from src.service.model.model_account import User


def user_details(userid):
    user = User.query.filter_by(id=userid).first()
    posts = User.query.order_by(User.id.desc()).limit(10)
    return user, posts
