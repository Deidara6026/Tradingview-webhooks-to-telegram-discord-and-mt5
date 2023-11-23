from django.shortcuts import render
from django.http import JsonResponse
from models import Signal

def signal_api_endpoint(request, _id):
    signal = Signal.objects.get(id=_id)
    if request.method == 'POST':
        data = request.POST
        tradingview_message = data.get('message')
        if signal.telegram_enabled:
            if signal.parse:
                tradingview_message = parse(tradingview_message, signal.telegram)
            telegram.send(tradingview_message, signal.telegram)
        # Forward the message to a telegram channel
        # Your code to forward the message to a telegram channel goes here
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
