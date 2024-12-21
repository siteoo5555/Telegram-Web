from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Confirmation)
admin.site.register(Chat)
admin.site.register(Photo)
admin.site.register(Messages)
admin.site.register(Profile)
admin.site.register(Chat_Link)