from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_login import current_user
from wtforms import validators
from flask import redirect, url_for, request

class MyModelView(ModelView):
    def is_accessible(self):
        # Yetkilendirme kontrolü yapılıyor
        # Örneğin, current_user.is_admin, kullanıcının yönetici olup olmadığını kontrol eden bir özellik olmalıdır
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        # Erişim reddedildiğinde ne yapılacağını belirleyin
        # Örneğin, kullanıcıyı giriş sayfasına yönlendirin
        return redirect(url_for('auth.login', next=request.url))
    
class UserModelView(MyModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]
