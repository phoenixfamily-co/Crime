from User.models import User


def get_or_create_temporary_user(request):
    if not request.session.get('user_id'):  # بررسی اینکه آیا کاربر قبلاً شناسایی شده است
        user = User.objects.create()  # ایجاد کاربر موقت
        request.session['user_id'] = str(user.id)  # ذخیره شناسه کاربر در سشن
    else:
        user = User.objects.get(id=request.session['user_id'])
    return user
