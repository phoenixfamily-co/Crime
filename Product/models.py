from django.db import models
from django.utils import timezone

from User.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    description = models.TextField(verbose_name="توضیحات دسته‌بندی", blank=True, null=True)

    def __str__(self):
        return self.name


class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان پرونده")
    description = models.TextField(verbose_name="شرح پرونده")
    image = models.ImageField(upload_to="images/", verbose_name='عکس پرونده', null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="محل وقوع")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت پرونده")
    report = models.TextField(verbose_name="گزارش پلیس")
    Video = models.FileField(upload_to='videos/', verbose_name="ویدیو پرونده", null=True, blank=True)
    result = models.TextField(verbose_name="دادنامه پرونده")
    active = models.BooleanField(blank=True, null=True, verbose_name='فعال', default=True)
    price = models.IntegerField(verbose_name="قیمت")

    age_range = models.CharField(
        max_length=5,
        choices=[
            ('G', 'G'),
            ('PG', 'PG'),
            ('PG-13', 'PG-13'),
            ('R', 'R'),
            ('NC-17', 'NC-17')
        ],
        verbose_name="رده سنی"
    )

    difficulty_number = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name="درجه سختی"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('easy', 'آسان'), ('medium', 'متوسط'), ('hard', 'سخت')],
        verbose_name="سطح سختی"
    )
    score = models.IntegerField(default=0, verbose_name="امتیاز", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی پرونده", null=True,
                                 blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.number}"

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.case.title} in cart {self.cart.id}"

    def total_price(self):
        return self.case.price * self.quantity


# Model for Orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.case.title} in order {self.order.id}"

    def total_price(self):
        return self.case.price * self.quantity


class GamePlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    OrderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'),
                                                      ('cancelled', 'Cancelled')],
                              default='in_progress')

    def __str__(self):
        return f"GamePlay of {self.OrderItem.case.title} by {self.user.number}"


class GameParticipant(models.Model):
    gameplay = models.ForeignKey(GamePlay, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participant {self.participant.number} in GamePlay {self.gameplay.id}"


class GameResult(models.Model):
    gameplay = models.OneToOneField(GamePlay, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])

    def __str__(self):
        return f"Result of GamePlay {self.gameplay.id}"


class Suspect(models.Model):
    case = models.ForeignKey(Case, related_name="suspect", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", verbose_name='عکس مظنون', null=True, blank=True)
    video = models.FileField(upload_to='videos/', verbose_name="ویدیو بازجویی", null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    murderer = models.BooleanField(verbose_name='قاتل', default=False)
    job = models.CharField(max_length=200, verbose_name="َشغل", blank=True, null=True)
    age = models.IntegerField(verbose_name="سن")
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'مرد'), ('female', 'زن')],
        verbose_name="جنسیت"
    )
    # قد
    height = models.FloatField(verbose_name="قد (سانتی‌متر)")
    # وزن
    weight = models.FloatField(verbose_name="وزن (کیلوگرم)")
    # گروه خونی
    blood_type = models.CharField(
        max_length=5,
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        verbose_name="گروه خونی"
    )
    # وضعیت تاهل
    marital_status = models.CharField(
        max_length=20,
        choices=[('single', 'مجرد'), ('married', 'متاهل'), ('divorced', 'طلاقت گرفته')],
        verbose_name="وضعیت تاهل"
    )
    relationship_with_victim = models.CharField(max_length=200, verbose_name="ارتباط با مقتول", blank=True, null=True)
    excuse = models.TextField(verbose_name="بهانه مظنون", blank=True, null=True)
    last_seen = models.TextField(verbose_name="آخرین بازدید", blank=True, null=True)

    def __str__(self):
        return self.name


class Evidence(models.Model):
    TYPE_CHOICES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
        ('VOICE', 'Voice'),
        ('OTHER', 'Other'),
    ]

    # ارتباط Evidence با CrimeCase
    case = models.ForeignKey(Case, related_name="evidences", on_delete=models.CASCADE)

    # ارتباط Evidence با Suspect
    suspect = models.ForeignKey(Suspect, related_name="evidences", on_delete=models.CASCADE, null=True, blank=True)

    # نوع مدرک
    evidence_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    title = models.CharField(max_length=200, verbose_name="عنوان مدرک")

    # توضیحات درباره مدرک
    description = models.TextField()

    # تاریخ و زمان ثبت مدرک
    date_collected = models.DateTimeField(default=timezone.now)

    # فایل ضمیمه (مدرک تصویری، ویدئویی یا دیگر فایل‌ها)
    file = models.FileField(upload_to='evidences/', null=True, blank=True)
    image = models.ImageField(upload_to="images/", verbose_name='عکس مدرک', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Locked', 'locked'), ('Unlocked', 'Unlocked')],
                              default='Unlocked')
    password = models.CharField(
        max_length=128,
        verbose_name="رمز عبور",
        null=True,
        blank=True,
        help_text="فقط برای مدارکی که قفل هستند استفاده می‌شود."
    )

    def __str__(self):
        return f"Evidence: {self.title} ({self.evidence_type})"

    def is_locked(self):
        return self.status == 'Locked'


class Interrogation(models.Model):
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, related_name="interrogations", verbose_name="مظنون")
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")
    heart_rate = models.IntegerField(verbose_name="ضربان قلب (بیت در دقیقه)", null=True, blank=True)

    # حالت چهره
    face_expression = models.CharField(
        max_length=50,
        choices=[('neutral', 'خنثی'), ('happy', 'خوشحال'), ('angry', 'عصبانی'),
                 ('sad', 'غمگین'), ('surprised', 'متعجب'), ('fearful', 'ترسیده'), ('nervous', 'نگران')],
        verbose_name="حالت چهره"
    )

    truth_level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name="میزان حقیقت (1 تا 10)",
        help_text="میزان حقیقت ادعاهای مظنون در بازجویی (1 = دروغ، 10 = حقیقت)"
    )

    def __str__(self):
        return f"بازجویی از {self.suspect.name}"
