from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
from blog.form import BlogForm, AuthorForm, ContactForm
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q



# Create your views here.


def Home(request):
    freature_blog = Blog.objects.filter(is_featured=True).first()
    page = request.GET.get('page')
    category =  request.GET.get('category')
    blogs_instance  = Blog.objects.prefetch_related('category').filter(is_published =  True)
    if category  is not None:
        blogs_instance = blogs_instance.filter( Q(category__category_name__icontains=category))

    all_blogs = Paginator(blogs_instance, 4)
    try:
        blogs = all_blogs.page(page)
    except PageNotAnInteger:
        blogs = all_blogs.page(1)
    except EmptyPage:
        blogs = all_blogs.page(all_blogs.num_pages)

    params = {'all_blogs': blogs, 'feature_post_data': freature_blog}

    return render(request, 'blogs/index.html', params)


def extract_table_of_content(html_content):
    anchor_tags_with_id = {}

    # Initialize BeautifulSoup with the provided HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all anchor tags (a elements) with an 'id' attribute
    anchor_tags = soup.find_all('a', id=True)

    # Extract the id attribute from each anchor tag
    for tag in anchor_tags:
        anchor_id = tag.get('id')
        anchor_tag_innner_text = tag.string
        anchor_tags_with_id[f'{anchor_id}'] = anchor_tag_innner_text

    return anchor_tags_with_id


def BlogDetail(request, slug):
    blog = Blog.objects.get(slug=slug)
    anchor_tags = extract_table_of_content(blog.content)
    comments = BlogComment.objects.filter(post_id=blog, parent_id=None)
    replies_instance = BlogComment.objects.filter(
        post_id=blog, parent_id__isnull=False).order_by('created_on')
    replies_dict = {}

    for reply in replies_instance:
        if reply.parent_id.id not in replies_dict.keys():
            replies_dict[reply.parent_id.id] = [reply]
        else:
            replies_dict[reply.parent_id.id].append(reply)

    blog.view_count += 1
    blog.save()
    return render(request, 'blogs/blog_detail.html', {'blog': blog, 'table_of_content': list(anchor_tags.items()), 'comments': comments, 'replies': replies_dict})


def Comment(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        comment = request.POST.get('comment')
        parent_comment_id = request.POST.get('parent_comment_id')
        print(blog_id)
        blog_instance = Blog.objects.get(id=blog_id)
        blog_instance.view_count -= 1

        if parent_comment_id is None or parent_comment_id == '':
            new_comment = BlogComment(
                user_id=request.user, post_id=blog_instance, comment=comment)
            new_comment.save()
            messages.success(
                request=request, message='Comment Has Been Added Successfully!!!')
        else:
            parent_comment = BlogComment.objects.get(id=parent_comment_id)
            new_comment = BlogComment(
                user_id=request.user, post_id=blog_instance, comment=comment, parent_id=parent_comment)
            new_comment.save()
            messages.success(
                request=request, message='Comment Has Been Added Successfully!!!')

    return redirect(f'/blog/{blog_instance.slug}')


@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def AddNewBlog(request):
    try:
        author = get_object_or_404(
            Author, is_verified=True, id=request.user.id)
        author_blogs = Blog.objects.prefetch_related(
            'category').filter(author_id=author)
        context = {
            'blogs': author_blogs
        }
    except Exception as e:
        messages.error(message="Un Authorize user Access", request=request)
        return redirect(reverse('login'))

    return render(request, 'blogs/list_blog.html', context)


@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def EditBlog(request, id):
    try:
        blog_data = get_object_or_404(Blog, id=id)
    except Exception as e:
        messages.error(message="Invalid Blog Data", request=request)
        return redirect(reverse('home'))

    try:
        author = get_object_or_404(
            Author, is_verified=True, id=request.user.id)
    except Exception as e:
        print(e)
        messages.error(message="Un Authorize user Access", request=request)
        return redirect(reverse('login'))

    if blog_data.author_id.id == author.id:
        if request.method == 'GET':
            context = {
                'form': BlogForm(instance=blog_data),
                'id': id,
                'form_title': 'Edit Blog',
                'blog': blog_data

            }
            return render(request, 'blogs/edit_blog.html', context)

        elif request.method == 'POST':
            form = BlogForm(request.POST or None, request.FILES or None, instance=blog_data)
            if form.is_valid():
                form.save()
                return redirect('list_blog')
            else:
                context = {
                    'form': BlogForm(instance=blog_data),
                    'id': id,
                    'form_title': 'Edit Blog',
                    'blog': blog_data


                }
            return render(request, 'blogs/edit_blog.html', context)

    else:
        messages.error(message="Un Authorize user Access", request=request)
        return redirect(reverse('login'))

    return render(request, 'blogs/edit_blog.html')



# @author_can_access
@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def NewBlog(request):
    context = {
                'form': BlogForm(),
                'form_title': 'Add Blog',

            }
    if request.method == 'POST':
        form = BlogForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(request_context =  request)
            return redirect('list_blog')
        else:
            context = {
                'form': BlogForm(request.POST or None, request.FILES or None),
                'form_title': 'Add Blog',
            }
            return render(request, 'blogs/edit_blog.html', context)
    
    return render(request, 'blogs/edit_blog.html', context)





@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def BeAnAuthor(request):
    
    try:
        author  =  get_object_or_404(Author, user_id =  request.user.id)
        if author.is_verified:
            messages.success(request, 'You Are Already An Author')
        else:
            messages.success(request, 'You Are Already Applied For Author')

        return redirect('edit_be_an_author', author.id)


    except Exception as e:
        context = {
                'form': AuthorForm(),
                'form_title': 'Be An Author',
            }


        if request.method =='POST':
            form  =  AuthorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Form Has been Submmitted. We will Contact you Shortly After Verification ')
                return redirect(reverse('home'))
            else:
                context = {
                    'form': AuthorForm(request.POST or None, request.FILES or None),
                    'form_title': 'Be An Author',
                }
                return render(request, 'blogs/be_an_author.html', context)

            

    return render(request, 'blogs/be_an_author.html', context=context)


@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def EditBeAnAuthor(request, id):
    try:
        author_data = get_object_or_404(Author, id=id, user_id = request.user.id)
        if request.method == 'GET':
            context = {
                'form': AuthorForm(instance=author_data),
                'id': id,
                'form_title': 'Edit Author',
                'author': author_data

            }

        elif request.method == 'POST':
            form = AuthorForm(request.POST or None, request.FILES or None, instance=author_data)
            if form.is_valid():
                form.save()
                return redirect(reverse('home'))
            else:
                context = {
                    'form': AuthorForm(instance=author_data),
                    'id': id,
                    'form_title': 'Edit Author',
                    'author': author_data


                }
    except Exception as e:
        messages.error(message="Invalid Author", request=request)
        return redirect(reverse('home'))
    
    return render(request, 'blogs/be_an_author.html', context)
    



def UnpublishBlog(request, id):
    try:
        author =  get_object_or_404(Author, user_id = request.user.id)
        blog = get_object_or_404(Blog, id=id, author_id = author.id)
        if blog.is_published == True:
            blog.is_published = False
            messages.success(request, 'Blog is UnPublished')

        else:
            blog.is_published = True
            messages.success(request, 'Blog is  Published')
        blog.save()
        return redirect(reverse('list_blog'))
        
    except Exception as e:
        messages.error(request, e)
        return redirect(reverse('list_blog'))
    

def DeleteBlog(request, id):
    try:
        author =  get_object_or_404(Author, user_id = request.user.id)
        blog = get_object_or_404(Blog, id=id, author_id = author.id)
        # categories  = get_object_or_404(Category, blog_id =  blog.id)
        blog.delete()
        messages.success(request, 'Blog is  Deleted')
        return redirect(reverse('list_blog'))
        
    except Exception as e:
        messages.error(request, e)
        return redirect(reverse('list_blog'))




def ContactView(request):
    context = {
                'form': ContactForm(),
                'form_title': 'Contact Us',
            }


    if request.method =='POST':
        form  =  ContactForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank your For your FeedBack')
            return redirect(reverse('home'))
        else:
            context = {
                'form': ContactForm(request.POST or None, request.FILES or None),
                'form_title': 'Contact Us',
            }
            return render(request, 'blogs/contact_us.html', context)

        

    return render(request, 'blogs/contact_us.html', context=context)

    



def AboutUs(request):

    return render(request, 'blogs/about.html')


def CategoriesView(request):
    categories  =  Category.objects.all()
    return render(request, 'blogs/categories.html', context= {'categories': categories})