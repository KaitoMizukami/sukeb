from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    # ユーザーインスタンスを追加、変更するためのフォーム
    form = UserChangeForm
    add_form = UserCreationForm

    # ユーザーモデルの表示に使用されるフィールド
    list_display = ('email', 'username', 'is_staff')
    fieldsets = (
        ('ユーザー情報', {
            'fields': (
                'username', 'email', 'password'
            )
        }),
        ('パーミッション', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )

    # ユーザーインスタンスを作成する時に必要なフィールド
    add_fieldsets = (
        ('ユーザー情報', {
            'fields': (
                'username','email', 'password', 'confirm_password'
            )
        }),
    )

    # 3つのフィールドでユーザーを絞り込む
    list_filter = ('is_staff', 'is_superuser', 'is_active',)

    # 検索される時に使われるフィールド
    search_fields = ('email', 'username',)


admin.site.register(get_user_model(), CustomUserAdmin) # 新しいユーザーアドミンを登録
admin.site.unregister(Group) # built-inのグループモデルを登録解除