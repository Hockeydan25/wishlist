from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage 

"""Create your models here.
blanks & null = True means doesn't have to be where as if we said False it would require it not be blank.
setting up the feilds that build  make a place object 
"""
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)  


    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()  # database query, if there is a new place
        if old_place and old_place.photo:
            if old_place.photo != self.photo:  # checking old phot validate not there or delete
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)  # takes two arguments, self is not and argument.        


    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)


    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)   

        super().delete(*args, **kwargs)     


    def __str__(self) -> str:  # string method list places visted not visited. this is visited
        photo_str = self.photo.url if self.photo else 'no photo'  # if phot or not setup here
        notes_str = self.notes[100:] if self.notes else 'no notes' # limitefd to 100 text count
        return f'{self.name} visted? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo: {photo_str}'


