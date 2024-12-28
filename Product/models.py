from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    description = models.TextField(verbose_name="توضیحات دسته‌بندی", blank=True, null=True)

    def __str__(self):
        return self.name


class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان پرونده")
    description = models.TextField(verbose_name="شرح پرونده")
    image = models.ImageField(upload_to="images/", verbose_name='عکس پرونده')
    location = models.CharField(max_length=200, verbose_name="محل وقوع")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت پرونده")
    report = models.TextField(verbose_name="گزارش پلیس")
    Video = models.FileField(upload_to='videos/', verbose_name="ویدیو پرونده")
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
    score = models.IntegerField(default=0, verbose_name="امتیاز")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی پرونده")

    def __str__(self):
        return self.title


class Suspect(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    murderer = models.BooleanField(verbose_name='قاتل', default=False)
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

    def __str__(self):
        return self.name


class Evidence(models.Model):
    TYPE_CHOICES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
        ('Voice', 'Voice'),
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

    status = models.CharField(max_length=20, choices=[('Locked', 'Unlocked'), ('Locked', 'Unlocked')],
                              default='Unlocked')

    def __str__(self):
        return f"Evidence: {self.evidence_type} for case {self.case.title}"


class Interrogation(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="interrogations", verbose_name="پرونده")
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
        return f"بازجویی از {self.suspect.name} در پرونده {self.case.title}"
