from django.contrib import admin

# Register your models here.
from .models import Listing
admin.site.register(Listing)

# Register your models here.
from .models import User
admin.site.register(User)

# Register your models here.
from .models import Category
admin.site.register(Category)

# Register your models here.
from .models import Coment
admin.site.register(Coment)