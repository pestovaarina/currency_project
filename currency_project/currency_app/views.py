from django.http import JsonResponse

import requests
import time
from collections import deque
from django_ratelimit.decorators import ratelimit

API_KEY = '9e6521ec12714457b4062179b9453b05'
last_10_requests = deque(maxlen=10)


@ratelimit(key='user', rate='1/10s', method=['GET'], block=False)
def get_current_usd(request):

    response = requests.get(f'https://openexchangerates.org/api/latest.'
                            f'json?app_id={API_KEY}&base=USD&symbols=RUB')
    data = response.json()
    usd_to_rub = data['rates']['RUB']

    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    last_10_requests.append({'time': current_time, 'usd_to_rub': usd_to_rub})

    return JsonResponse({'usd_to_rub': usd_to_rub,
                         'last_10_requests': list(last_10_requests)})
