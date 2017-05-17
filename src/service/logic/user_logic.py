from src.service.model.db_connection import connection, execute_total
from src.service.logic.util_logic import UtilLogic, ListFilter
from src.service.model.model_account import User


class UserLogic(UtilLogic):
    def new(self, new_user):
        self._verify_except_case()

        connection.add(new_user)
        connection.commit()
        return True

    def update(self, user):
        self._verify_except_case()

        connection.query(User).filter_by(id=user.id).update({
            User.username: user.username,
            User.password: user.password
        })
        connection.commit()
        return True

    def delete(self, user):
        self._verify_except_case()

        connection.delete(user)
        connection.commit()
        return True

    def get_detail(self, user_id):
        self._verify_except_case()

        try:
            _user = connection.query(User).filter_by(id=user_id).first()  # .one()

        except Exception as ex:
            print(str(ex)[0:500])

        return _user

    def get_detail_by_auth(self, user_name):
        self._verify_except_case()

        try:
            _user = connection.query(User).filter_by(account_name=user_name).first()  # .one()
            _user.is_authenticated()

        except Exception as ex:
            print(str(ex)[0:500])

        return _user

    def get_list(self, list_filter=None):
        try:
            if list_filter is None:
                list_filter = ListFilter()

            _filter_sql = list_filter.filter_sql + " order by UserID desc " + list_filter.offset_limit_sql
            _listResult = connection.query(User).filter(_filter_sql)
            _total = execute_total(User.__tablename__, list_filter.filter_sql)

        except Exception as ex:
            raise RuntimeError(ex)

        return self.new_result_page(_listResult, list_filter, _total)


def user_details(userid):
    user = User.query.filter_by(id=userid).first()
    posts = User.query.order_by(User.id.desc()).limit(10)
    return user, posts
