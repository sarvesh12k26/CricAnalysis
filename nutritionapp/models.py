from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    height = models.IntegerField(null=True)  # in inch
    activity_level = models.IntegerField(null=True)   # eg very light, light, moderate, heavy, very heavy
    body_fat = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Weight(models.Model):
    user = models.ForeignKey(User, related_name='userweight', on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=1, max_digits=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class BMI(models.Model):
    user = models.ForeignKey(User, related_name='userbmi', on_delete=models.CASCADE)
    bmi = models.DecimalField(decimal_places=2, max_digits=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class MacroNutrient(models.Model):                          # for daily macronutrients requirements
    user = models.ForeignKey(User, related_name='usermacronutrient', on_delete=models.CASCADE)
    proteins = models.IntegerField()  # in grams
    carbs = models.IntegerField()
    fats = models.IntegerField()
    calories = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Food(models.Model):
    user = models.ForeignKey(User, related_name='userfood', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    meal_type = models.IntegerField()  # eg breakfast, lunch, evening snacks, dinner
    calories = models.DecimalField(decimal_places=2, max_digits=6)
    servings = models.IntegerField()
    carbs = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    # calcium = models.IntegerField()  # in percent
    # cholestrol = models.IntegerField()  # in mg

    def __str__(self):
        return self.user.username


class Water(models.Model):
    user = models.ForeignKey(User, related_name='userwater', on_delete=models.CASCADE)
    water = models.IntegerField()  # in glasses
    on_date=models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    type = models.CharField(max_length=20)   # eg very light, light, moderate, heavy, very heavy
    description=models.CharField(max_length=2048, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class MealType(models.Model):
    type = models.CharField(max_length=20)  # eg breakfast, lunch, dinner, evening snacks
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

