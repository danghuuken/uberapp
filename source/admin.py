from django.contrib import admin
from source.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	#fields displayed on change list
	list_display = ['title','description']

	list_filter = ['published','created']

	search_fields = ['title', 'description', 'content']

	date_hierarchy = 'created'

	save_on_top = True

	prepopulated_fileds = {"slug" : ("title",)}

admin.site.register(Post,PostAdmin)