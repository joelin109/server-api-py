from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os

from webapp.server.model.model_content import db, ContentArticle, ContentDictionary, ContentChannel
from webapp.server.model.model_account import User
from webapp.uicontroller.custom_form import CKTextAreaField

_admin = Admin()


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):
    def is_accessible(self):
        return True


class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return True
        # return current_user.is_


class AdminArticleView(CustomModelView):
    form_overrides = dict(text=CKTextAreaField)
    column_searchable_list = ('format_type', 'title')
    column_filters = ('create_date',)

    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


class LogOut(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/second_page.html')


# Public Register def
def register_admin(app):
    _admin.init_app(app)

    _admin.add_view(CustomView(name='CustomJ'))
    _admin.add_view(
        CustomModelView(
            User, db.session, category='Models'
        )
    )
    _admin.add_view(
        CustomModelView(
            ContentChannel, db.session, category='Models'
        )
    )
    _admin.add_view(
        CustomModelView(
            ContentDictionary, db.session, category='Models'
        )
    )
    _admin.add_view(
        AdminArticleView(
            ContentArticle, db.session, category='Models'
        )
    )
    _admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), '../static'),
            '/static/',
            name='Static Files'
        )
    )
    _admin.add_view(LogOut(name='LogOut'))
