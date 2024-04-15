from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, phone, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone = models.CharField(max_length=20, default=None, null=True, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Custom fields
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Adjust this method to check user permissions based on roles
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Adjust this method to check user permissions based on roles
        return self.is_superuser


class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'
    EXPENSE_TYPES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='expenses_paid')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    participants = models.ManyToManyField(UserProfile, through='ExpenseSplit', related_name='expenses_participated')
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.expense_type == self.EQUAL:
            participants_count = self.expensesplit_set.count() + 1  # Including the user who paid
            share_per_participant = self.amount / participants_count
            for split in self.expensesplit_set.all():
                if split.amount_owed != share_per_participant:
                    raise ValidationError("For EQUAL expense, each participant must owe the same amount")

        elif self.expense_type == self.EXACT:
            total_share = sum(split.amount_owed for split in self.expensesplit_set.all())
            if total_share != self.amount:
                raise ValidationError("Total amount of shares must equal the expense amount")

        elif self.expense_type == self.PERCENT:
            total_percent = sum(split.amount_owed for split in self.expensesplit_set.all())
            if total_percent != 100:
                raise ValidationError("Total percentage shares must add up to 100")

class Balance(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='balance_owner')
    # owes_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='balance_owed_to')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_splits')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
