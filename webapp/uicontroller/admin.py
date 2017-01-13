from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user

from webapp.server.model.model_content import db, ContentArticle, ContentDictionary, ContentChannel
from webapp.uicontroller.extension import (admin_permission, f_admin)


# from webapp.forms import CKTextAreaField


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):
    pass


class PostView(CustomModelView):
    # form_overrides = dict(text=CKTextAreaField)
    column_searchable_list = ('text', 'title')
    column_filters = ('publish_date',)

    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()


# Public Register def
def register_admin(app):
    f_admin.init_app(app)

    f_admin.add_view(CustomView(name='CustomJ'))
    f_admin.add_view(
        CustomModelView(
            ContentDictionary, db.session, category='Models'
        )
    )
    f_admin.add_view(
        CustomModelView(
            ContentChannel, db.session, category='Models'
        )
    )
