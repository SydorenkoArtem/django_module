from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=False, blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["category"]

    def __repr__(self):
        """Return a string representation of a model"""

        return f"<Category ({self.pk}) {self}>"

    def __str__(self):
        """Return a string version of an instance"""

        return self.category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    """Product model implementation"""

    fid = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    pic = models.ImageField(upload_to="product")
    amount = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = "product"
        ordering = ["category", "price"]

    def __repr__(self):
        """Return a string representation of an instance"""

        return f"<Product ({self.pk}) '{self}'>"

    def __str__(self):
        """Return a string version of an instance"""

        return self.product

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product)
        if self.amount < 0:
            self.amount = 0

        super(Product, self).save(*args, **kwargs)

