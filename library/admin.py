from django.contrib import admin
from library.models import Category, Book, Review, Notification, BorrowRequest, ExtensionRequest, ReviewRequest, \
    History

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(BorrowRequest)
admin.site.register(ExtensionRequest)
admin.site.register(ReviewRequest)
admin.site.register(History)
