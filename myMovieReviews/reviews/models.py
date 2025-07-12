from django.db import models

class Review(models.Model):
    GENRE_CHOICES = [('SF', 'SF'), ('Action', 'Action'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('Romance', 'Romance'), ('Horror', 'Horror'), ('Animation', 'Animation'), ('Documentary', 'Documentary')]
    title = models.CharField('제목', max_length=200)  # 영화 제목
    release_year = models.IntegerField('개봉년도')  # 개봉년도
    genre = models.CharField('장르', max_length=100, choices=GENRE_CHOICES)
    rating = models.FloatField('별점')  # 별점 (예: 4.5)
    runtime = models.IntegerField('러닝타임')  # 러닝타임(분)
    director = models.CharField('감독', max_length=100)
    cast = models.CharField('배우', max_length=200)  # 주연
    content = models.TextField('리뷰')  # 리뷰 내용
    poster_url = models.URLField('포스터 URL', blank=True)  # 포스터 이미지 (선택 사항)
    created_at = models.DateTimeField('작성일', auto_now_add=True)


