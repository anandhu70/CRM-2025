import random

import string

# to avoid multiple adm num

from students.models import Students

# to send email

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from decouple import config

from twilio.rest import Client

from django.utils import timezone









def generate_admission_number():

    five_numbers=''.join(random.choices(string.digits,k=5))

    adm_num=f'LM-{five_numbers}'

    if not  Students.objects.filter(adm_num=adm_num).exists():

        return adm_num
    


def generate_password():

    password=''.join(random.choices(string.ascii_lowercase+string.ascii_uppercase,k=5))

    return password



#  for  email

def sent_mail(recepient,template,context,title):

    sender=config('EMAIL_HOST_USER')

    content=render_to_string(template,context)    #renderto string used to convert string (html accepts only text)
                                                       
    msg=EmailMultiAlternatives(from_email=sender,to=[recepient],subject=title)  #[] to writeas list so n emails
        # using EmailMultiAlternatives to implement designs or pages (not plain text )

    msg.attach_alternative(content,'text/html')   

    msg.send() 


# to generate otp

def generate_otps():

    email_otp=''.join(random.choices(string.digits,k=4))

    phone_otp=''.join(random.choices(string.digits,k=4))

    return email_otp,phone_otp



# def send_otp_sms(phone_num,otp):  normal case 

def send_otp_sms(otp):

    account_sid = config('account_sid')

    auth_token = config('AUTH_TOKEN')

    from_num=config('FROM_NUM')

    client = Client(account_sid, auth_token)
    message = client.messages.create(from_=from_num,
    to='+917510708783',

    body=f'OTP for verification: {otp}')

    # for masking email and Phone 

def masking_email_and_phone(email,phone):

    username,domain=email.split('@') 

    remaining_part=username[5:]

    remaining_part_phone=phone[-4:]

    masked_email=f'*****{remaining_part}@{domain}'  

    masked_phone=f'******{remaining_part_phone}'

    return masked_email,masked_phone 


def get_batch_code(course,start_date):

    month_codes={1:'JAN',
                 2:'FEB',
                 3:'MAR',
                 4:'APR',
                 5:'MAY',
                 6:'JUN',
                 7:'JUL',
                 8:'AUG',
                 9:'SEP',
        
                 10:'OCT',
                 11:'NOV',
                 12:'DEC'
                 
                 



    }


    course_code= course.code

    month=start_date.month

    year=start_date.year

    if month in month_codes:

        month_code=month_codes.get(month)

        return f'{course_code}-{month_code}-{year}'
    
def get_end_date(start_date):

    return start_date+timezone.timedelta(days=180)







  






