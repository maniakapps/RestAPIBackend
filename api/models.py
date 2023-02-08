class Company(models.Model):
    """A class that models a company"""
    name = models.CharField("The name of company", max_length=200, unique=True)
    website = models.URLField("The website of the company", max_length=200, default="", blank=True)
    foundation = models.DateField("The date of foundation")
    description = models.TextField("A brief description of the company", blank=True)
    logo = models.ImageField("The company logo", upload_to='logos/', blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        """Returns a string representation of the company"""
        return self.name

    class Meta:
        ordering = ['name']
