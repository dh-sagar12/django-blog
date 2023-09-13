from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from authentication.models import User




# Create your models here.
class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    address  =  models.CharField(max_length=100, null=False, blank=False)
    contact_number =  models.CharField(max_length=10, null=False, blank=False)
    about_you   = models.TextField(null=False, blank=False)
    user_id =  models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False, db_column='user_id', related_name='user_id')
    is_verified =  models.BooleanField(default=False)
    verified_by =  models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, db_column='verified_by', related_name='verified_by')
    
    class Meta:
        db_table = 'authors'
        verbose_name = "Author"
        verbose_name_plural = 'Authors'

    def __str__(self) -> str:
        return self.name




class Category(models.Model):
    id =  models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        db_table = 'categories'
        verbose_name = "Cateogory"
        verbose_name_plural = 'Cateogories'


    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("category", kwargs={"id": self.id})

class CategoryBlog(models.Model):
    id =  models.BigAutoField(primary_key=True)
    category_id =  models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=False, blank=False, db_column='category_id')
    blog_id =  models.ForeignKey("Blog", on_delete=models.CASCADE, null=False, blank=False, db_column='blog_id')


    class Meta:
        db_table = 'blog_categories'
        verbose_name = "Blog Category"
        verbose_name_plural = 'Blog Cateogories'




class Blog(models.Model):
    id =  models.BigAutoField(primary_key=True)
    title =  models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=False,  null=False)
    content = RichTextField(blank= False, null= False)
    author_id = models.ForeignKey(Author, on_delete=models.DO_NOTHING, blank=False, null=False, db_column='author_id' )
    category = models.ManyToManyField(Category, through=CategoryBlog, related_name='blog_category' )
    upload_date = models.DateTimeField(auto_now_add=True)
    view_count= models.IntegerField(default=0, db_column='view_count')
    thumbnail = models.ImageField(upload_to= 'Blog/Images')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    like_count  =  models.IntegerField(default=0,  null=False, blank=False)
    uploaded_by =  models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False, db_column='uploaded_by')

    class Meta:
        ordering = ['-upload_date']
        db_table = 'blogs'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})



class BlogComment(models.Model):
    id = models.BigAutoField(primary_key= True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    post_id = models.ForeignKey(Blog, on_delete= models.DO_NOTHING, db_column='post_id')
    comment = models.TextField()
    parent_id= models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, db_column='parent_id' )
    is_edited =  models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        db_table  = 'blog_comments'

    def __str__(self):
        return self.comment[0:13] + "..." + "by " + self.user_id.first_name
    



class Contact(models.Model):
    id =  models.BigAutoField(primary_key=True)
    email =  models.EmailField(null=False)
    full_name = models.CharField(max_length=50)
    message = models.TextField(null=False)
    created_on  =  models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-created_on']
        db_table = 'contact'

    def __str__(self):
        return self.email