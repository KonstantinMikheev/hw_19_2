from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm, BlogModeratorForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # queryset = queryset.filter(is_published=True)  # Скрывает деактивированные статьи
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 100:
            send_mail(
                subject='Поздравляем!',
                message=f'Количество просмотров поста "{self.object.title}" достигло 100',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['konstantin_mikheev@mail.ru'],
            )
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Метод для выбора формы в зависимости от прав доступа пользователя"""
        user = self.request.user  # Получаем текущего пользователя
        if user == self.object.author:
            return BlogForm
        elif user.has_perm('blog.can_edit_is_published') and user.has_perm(
                'blog.can_edit_body') and user.has_perm('blog.can_edit_title') and user.has_perm(
            'blog.can_edit_preview') or user.is_superuser:
            return BlogModeratorForm
        else:
            raise PermissionDenied


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


@login_required
@permission_required
def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()
    return redirect(reverse('blog:list'))
