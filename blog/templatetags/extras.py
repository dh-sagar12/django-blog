from django import template

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