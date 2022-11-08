from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, name, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('É preciso informar o e-mail')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, password=password, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password, **extra_fields):
        return self._create_user(name, email, password, False, False, **extra_fields)

    def create_superuser(self, name, email, password, **extra_fields):
        user = self._create_user(name, email, password, True, True, **extra_fields)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', max_length=64, unique=True)
    name = models.CharField('Nome', max_length=64)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Ambition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField('Cidade', max_length=64)
    course = models.CharField('Curso', max_length=64)
    college = models.CharField('Faculdade', max_length=64)
    math_weight = models.PositiveSmallIntegerField('Peso de Matemática', default=1)
    languages_weight = models.PositiveSmallIntegerField('Peso de Linguagens', default=1)
    science_weight = models.PositiveSmallIntegerField('Peso de Ciências da Natureza', default=1)
    human_science_weight = models.PositiveSmallIntegerField('Peso de Ciências Humanas', default=1)
    essay_weight = models.PositiveSmallIntegerField('Peso de Redação', default=1)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.course} - {self.college} - {self.city}'

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'


class BetterChoices(models.IntegerChoices):
    @classmethod
    def get_value(cls, label):
        try:
            labels = [lbl.lower() for lbl in cls.labels]
            pos = labels.index(label.lower())
            return cls.values[pos]
        except ValueError:
            return None

    @classmethod
    def get_label(cls, value):
        try:
            pos = cls.values.index(value)
            return cls.labels[pos]
        except ValueError:
            return None


class ScoreChoices(BetterChoices):
    SIMULATION = 0, 'Simulação'
    OFFICIAL = 1, 'Nota oficial'


class Simulation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ambition = models.ForeignKey(Ambition, on_delete=models.CASCADE)
    name = models.CharField('Nome da simulação', max_length=64)
    math = models.FloatField('Nota de Matemática', default=0)
    languages = models.FloatField('Nota de Linguagens', default=0)
    science = models.FloatField('Nota de Ciências da Natureza', default=0)
    human_science = models.FloatField('Nota de Ciências Humanas', default=0)
    essay = models.FloatField('Nota de Redação', default=0)
    official_score = models.PositiveSmallIntegerField('Nota Oficial', choices=ScoreChoices.choices)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.name} - {self.ambition}'

    class Meta:
        verbose_name = 'Simulação'
        verbose_name_plural = 'Simulações'
