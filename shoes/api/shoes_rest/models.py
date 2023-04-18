from django.db import models
from django.urls import reverse

# Create your models here.
class BinVO(models.Model):
    import_id = models.CharField(max_length=200, unique=True)
    closet_name = models.CharField(max_length=200)

class Shoe(models.Model):
    manufacturer = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=200)
    bin = models.ForeignKey(
        BinVO,
        related_name="shoes",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.model_name

    def get_api_url(self):
        return reverse("api_list_shoes", kwargs={"pk": self.pk})
