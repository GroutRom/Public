from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Band(models.Model) :

	class Genre(models.TextChoices):
		HIP_HOP = 'HH'
		SYNT_POP ='SP'
		ALTERNATIVE_ROCK = 'AR'
		POP = 'POP'
		ROCK = 'RK'
		JAZZ = 'JZZ'
		BLUES = 'BLS'
		CLASSICAL = 'CLASS'
		COUNTRY = 'CNTRY'
		ELECTRONIC = 'ELEC'
		REGGAE = 'REG'
		FUNK = 'FK'
		METAL = 'MTL'
		RNB = 'RNB'
		SOUL = 'SL'
		FOLK = 'FO'
		LATIN = 'LAT'
		PUNK = 'PU'
		GOSPEL = 'GOS'
		RAP = 'RP'

	name = models.CharField(max_length=100)
	genre = models.CharField(max_length=50, choices=Genre.choices)
	biography = models.CharField(max_length=1000)
	year_formed = models.IntegerField(validators=[MinValueValidator(1900),
		MaxValueValidator(2024)])
	active = models.BooleanField(default=True)
	official_homepage = models.URLField(null=True, blank=True)
	

	def __str__(self):
		return f'{self.name}'

class Ad(models.Model) :

	class Type(models.TextChoices):
		RECORDS = 'Records'
		CLOTHING = 'Clothing'
		POSTERS = 'Posters'
		DIVERS = 'Miscellaneous'

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	sold = models.BooleanField(default=False)
	year = models.IntegerField(null=True,validators=[MinValueValidator(1900),
		MaxValueValidator(2024)])
	types = models.CharField(max_length=50, choices=Type.choices)
	band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return f'{self.title}'