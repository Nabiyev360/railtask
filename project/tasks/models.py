from django.db import models

from profiles.models import Profile


class Task(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Topshiriq berildi'),
        ('accepted', 'Qabul qilindi'),
        ('in_progress', 'Bajarilmoqda'),
        ('completed', 'Bajarildi'),
        ('approved', 'Tasdiqlandi'),
        ('expired', 'Bajarilmadi'),
        ('returned', 'Qayta ishlashga yuborildi'),
    ]

    DEGREE_CHOICES = [
        ('info', "Ma'lumot uchun"),
        ('medium', "O'rtacha"),
        ('important', "Muhim"),
        ('very_important', "Juda muhim"),
        ('urgent', "Tezkor"),
    ]

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    performers = models.ManyToManyField(Profile, related_name='performers')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    received = models.DateField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES, default='medium')
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskComment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment