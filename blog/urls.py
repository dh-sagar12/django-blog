from django.urls import path
from . import views



urlpatterns = [
    path("", views.Home, name="home"),
    path("blog/<str:slug>/", views.BlogDetail, name="blog_detail"),
    path("comment/", views.Comment, name="blog_comment"),
    path("contact/", views.ContactView, name="contact_us"),
    path("my-blog/", views.AddNewBlog, name="list_blog"),
    path("my-blog/<int:id>", views.EditBlog, name="edit_blog"),
    path("my-blog/new/", views.NewBlog, name="add_blog"),
    path("be-an-author/", views.BeAnAuthor, name="be_an_author"),
    path("be-an-author/<int:id>", views.EditBeAnAuthor, name="edit_be_an_author"),
    path("blog/unpublish/<int:id>/", views.UnpublishBlog, name="unpublish_blog"),
    path("blog/delete/<int:id>/", views.DeleteBlog, name="delete_blog"),
    path("about/", views.AboutUs, name="about_us"),
    path("categories/", views.CategoriesView, name="categories"),

]