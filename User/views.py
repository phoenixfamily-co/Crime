import json
import uuid
from django.http import JsonResponse
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent
from User.models import User, UserDeviceInfo, UserActivityLog
from django.contrib.auth import login
from django.utils.crypto import get_random_string


def get_or_create_temporary_user(request):

    if not request.session.get('user_id'):  # بررسی اینکه آیا کاربر موقت در سشن ذخیره شده است
        user = User.objects.create(
            id=uuid.uuid4(),
            first_name='Temporary',
            last_name=f'User-{get_random_string(6)}',
            is_temporary=True,
            is_active=True,
        )
        request.session['user_id'] = str(user.id)  # ذخیره شناسه کاربر در سشن
        login(request, user)  # لاگین کاربر موقت
    else:
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id, is_temporary=True)
            login(request, user)  # اطمینان از لاگین کاربر موقت
        except User.DoesNotExist:
            user = get_or_create_temporary_user(request)  # در صورت عدم وجود، کاربر جدید ایجاد می‌شود
    return user


def get_device_info(request):
    user_agent = get_user_agent(request)
    ip_address = get_client_ip(request)

    return {
        'device_type': 'Mobile' if user_agent.is_mobile else 'Tablet' if user_agent.is_tablet else 'Desktop' if
        user_agent.is_pc else 'Unknown',
        'device_model': user_agent.device.family,
        'operating_system': user_agent.os.family,
        'os_version': user_agent.os.version_string,
        'browser': user_agent.browser.family,
        'browser_version': user_agent.browser.version_string,
        'ip_address': ip_address,
        'country': None,  # این بخش در مرحله بعد اضافه می‌شود
        'city': None,  # این بخش در مرحله بعد اضافه می‌شود
    }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
    return ip


def save_user_device_info(request, user):
    if not UserDeviceInfo.objects.filter(user=user).exists():
        device_info = get_device_info(request)

        UserDeviceInfo.objects.create(
            user=user,
            device_type=device_info['device_type'],
            device_model=device_info['device_model'],
            operating_system=device_info['operating_system'],
            os_version=device_info['os_version'],
            browser=device_info['browser'],
            browser_version=device_info['browser_version'],
            ip_address=device_info['ip_address'],
            country=device_info['country'],
            city=device_info['city'],
        )


def log_user_activity(request, visited_page, user):
    # ثبت لاگ فعالیت
    activity_log = UserActivityLog.objects.create(
        user=user,
        visited_page=visited_page,
        entry_time=now(),
    )
    return activity_log


def log_exit_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        activity_log_id = data.get('activity_log_id')
        exit_time = data.get('exit_time')

        try:
            log = UserActivityLog.objects.get(id=activity_log_id)
            log.exit_time = exit_time
            log.save()
            return JsonResponse({'status': 'success'})
        except UserActivityLog.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Log not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
