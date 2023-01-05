from django.contrib import admin
from book.models import Publisher,Book,Author

admin.site.register([Publisher,Book,Author])