from django.contrib import admin

from .models import Post, Skatepark, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 投稿モデルの表示に使用されるフィールド
    list_display = ('author', 'skatepark', 'body',)
    fieldsets = (
        ('投稿', {
            'fields': (
                'author', 'skatepark', 'body',
            )
        }),
    )
     # 1つのフィールドでユーザーを絞り込む
    list_filter = ('author',)

    # 検索される時に使われるフィールド
    search_fields = ('author', 'skatepark',)


@admin.register(Skatepark)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefecture', 'city')
    fieldsets = (
        ('スケートパーク', {
            'fields': (
                'name', 
                'prefecture',
                'city',
                'skatepark_image',
            )
        }),
    )
    # 2つのフィールドでユーザーを絞り込む
    list_filter = ('prefecture', 'city',)

    # 検索される時に使われるフィールド
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_at')
    fieldsets = (
        ('コメント', {
            'fields': (
                'post',
                'author',
                'body',
            )
        }),
    )
    list_filter = ('author', 'created_at', )
    search_fields = ('author',)