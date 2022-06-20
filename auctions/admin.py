from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bid, Comment, Listing, Tag, User,  Watchlist

class ListingAdmin(admin.ModelAdmin):
    list_display = ("post_title", "user", "id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "body")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "dollar")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
admin.site.register(Tag)