# for custom template fncts  according  role permissions

# help of library class 

from django.template import Library

register= Library()


# @register.simple_tag 
# def display_name():

#     return 'anandhu'
# @register.simple_tag 
# def display_name(name):

    # return name.upper()

#  if there is parametre function_name(space) 'parametre',par2 as name 
 
@register.simple_tag

def check_roles(request,roles):

    roles=roles.split(',')

    if request.user.is_authenticated and request.user.role in roles:

        return True
    
    return False
