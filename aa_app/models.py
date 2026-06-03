from django.db import models



class Artist(models.Model):
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=50)
    artist = models.BooleanField(default=True)
    category = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pic = models.FileField(max_length=100, upload_to='Artists/', default='')

    def __str__(self) -> str:
        return self.name    
    


class User(models.Model):
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=50)
    user = models.BooleanField(default=True)
    email = models.CharField(max_length=50)
    pic = models.FileField(max_length=100, upload_to='Users/', default='')

    def __str__(self) -> str:
        return self.name



class Portal(models.Model):
    pid = models.CharField(max_length=32)
    admin = models.BooleanField(default=True)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=50, default="Admin")



class Video(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=50)
    desc = models.TextField(default="")
    link = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self) -> str:
        return self.name


class Pdf(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=50)
    desc = models.TextField(default="")
    link = models.FileField(max_length=200, upload_to='PDFs/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self) -> str:
        return self.name


class Art(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    pic = models.FileField(max_length=100, upload_to='Arts/', default='')
    art_type = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    desc = models.TextField()
    forsale = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created']



class Query(models.Model):
    name = models.CharField(max_length=50, default="Annonymous")
    email = models.CharField(max_length=50, default="")
    question = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    art = models.ForeignKey(Art, on_delete=models.DO_NOTHING)
    rating = models.CharField(max_length=10, default="")
    review = models.TextField(default="")

    def __str__(self) -> str:
        return self.art.name
    




class Event(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING, null=True)
    admin = models.ForeignKey(Portal, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50, default="")
    date = models.CharField(max_length=50,default="")
    venue = models.CharField(max_length=50, default="")
    pic = models.FileField(max_length=100, upload_to='Events/', default='')



class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)
    user_message = models.TextField(null=True, blank=True)
    artist_message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return "MessageID: "+str(self.id)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    art = models.ForeignKey(Art, on_delete=models.DO_NOTHING)
    payment = models.FileField(max_length=100, upload_to='Payments/', default='')
    status = models.CharField(max_length=50, default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.art.name
    