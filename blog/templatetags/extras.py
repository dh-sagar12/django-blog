from django import template

from blog.models import Blog

register = template.Library()

@register.filter(name= 'min_to_read')
def min_to_read(value):
    return len(value.split()) // 200 



@register.filter(name= 'get_val')
def get_val(item):
    return item[1]

@register.filter(name= 'get_key')
def get_key(item):
    return item[0]

@register.filter(name='get_reply')
def get_reply(replies, reply_id):
    return replies.get(reply_id)

@register.filter(name='liked')
# @register.inclusion_tag('blogs/blog_details.html', takes_context=True)
def liked(blog, user):
    # liked =  blog.like_count.filter(user_id=  user.id).exists()
    liked =  blog.like_count.filter(id= user.id).exists()
    return liked
 