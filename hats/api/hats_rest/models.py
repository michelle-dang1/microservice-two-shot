from django.db import models
from django.urls import reverse

class LocationVO(models.Model):
    import_id = models.CharField(max_length=200, unique=True)
    closet_name = models.CharField(max_length=200)

    def __str__(self):
        return self.closet_name

class Hat(models.Model):
    fabric = models.CharField(max_length=100)
    style_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=200)
    location = models.ForeignKey(
        "LocationVO",
        related_name="hats",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.style_name

    def get_api_url(self):
        return reverse("api_list_hats", kwargs={"pk": self.pk})
