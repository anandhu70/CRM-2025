import random

import string

# to avoid multiple adm num

from students.models import Students



def generate_admission_number():

    five_numbers=''.join(random.choices(string.digits,k=5))

    adm_num=f'LM-{five_numbers}'

    if not  Students.objects.filter(adm_num=adm_num).exists():

        return adm_num

