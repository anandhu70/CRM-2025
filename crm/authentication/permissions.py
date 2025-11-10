# permitted users ('admin','sales)

# to redirect 

from  django.shortcuts import redirect

from django.contrib import messages

# new decorators so a new parametere to take list  to pass para to decorator 

def permited_users(roles):

    # to take function

    def  decorator(fn):

        def wrapper(request,*args,**kwargs):

            if request.user.is_authenticated:

                if request.user.role in roles:

                    return fn (request,*args,**kwargs)
                
                else :

                    messages.error(request,'you have no Permission ')

                    return redirect('dashboard')

                


            else:

                return redirect('login')
            

        return wrapper 
    return decorator           


