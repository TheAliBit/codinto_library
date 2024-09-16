from django.contrib import admin
from library.models import Category, Book, ReviewRequest, Notification, BorrowRequest, ExtensionRequest, ReviewRequest, \
    History, ReturnRequest, BaseRequestModel

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(ReviewRequest)
admin.site.register(Notification)
admin.site.register(BorrowRequest)
admin.site.register(ExtensionRequest)
admin.site.register(ReturnRequest)
admin.site.register(History)
admin.site.register(BaseRequestModel)
