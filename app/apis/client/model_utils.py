from app.models.client import User
def get_user(ident):
    '''
    通过ID，用户名，邮箱，手机号码识别用户
    '''
    user = User.query.get(ident)
    if user:
        return user
    user = User.query.filter(User.username == ident).first()
    if user:
        return user
    user = User.query.filter(User.phone == ident).first()
    if user:
        return user
    user = User.query.filter(User.email == ident).first()
    if user:
        return user
    return None