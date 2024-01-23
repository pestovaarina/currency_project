import time

import requests
from django.http import JsonResponse
from collections import deque
from django_ratelimit.decorators import ratelimit

from currency_project.settings import API_KEY, MAX_LEN

last_10_requests = deque(maxlen=MAX_LEN)


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
