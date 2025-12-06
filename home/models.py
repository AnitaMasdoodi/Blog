from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            unique_slug = new_slug
            num = 1

            # بررسی می‌کنیم که آیا این `slug` قبلاً در دیتابیس وجود دارد یا نه
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{new_slug}-{num}"
                num += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    image = models.ImageField(upload_to='media')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=225)
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            unique_slug = new_slug
            num = 1

            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{new_slug}-{num}"
                num += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    def total_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='upost')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}' 
    
    class Meta:
        ordering = ['-date']
    

class Aboutme(models.Model):
    image = models.ImageField(upload_to='media')
    text = models.TextField()

    def __str__(self):
        return f'{self.text}'