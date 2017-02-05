from wtforms import widgets, StringField, TextAreaField, PasswordField, BooleanField


class CKTextAreaWigdet(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWigdet, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWigdet()
