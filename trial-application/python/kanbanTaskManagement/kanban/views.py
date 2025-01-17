from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm 
from .models import List, Card
from .mixins import OnlyYouMixin

def index(request):
    return render(request, "kanban/index.html")

# @login_required
# def home(request):
#     return render(request, "kanban/home.html")


def signup(request):
    if request.method == 'POST':
      # POSTの場合（サインアップのリクエストが送信された場合）
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("kanban:home")
      # GETの場合（通常のリクエストで情報記入へ）
    else:
        form = UserCreationForm()
        context = {
            "form": form
        }
    return render(request, 'kanban/signup.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "kanban/users/detail.html"

class UserUpdateView(OnlyYouMixin, UpdateView): 
    model = User
    template_name = "kanban/users/update.html"
    form_class = UserForm

    def get_success_url(self):
      # ビューの名称とPKの値をもとに、 /kanban/users/1/ といったURLに変換する処理
        return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])


class ListCreateView(LoginRequiredMixin, CreateView):
  model = List
  template_name = "kanban/lists/create.html"
  form_class = ListForm
  success_url = reverse_lazy("kanban:lists_list")

  def form_valid(self, form):
    """フォームで作成されるインスタンスに user フィールドを追加し、
    そこにリクエストしたユーザーアカウント request.user を保存している。
    このようにすることで、フォーム作成時にあえて定義しなかった
    ユーザーに関する情報を保存することが可能"""
    form.instance.user = self.request.user
    return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
  model = List
  template_name = "kanban/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
  model = List
  template_name = "kanban/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
  model = List
  template_name = "kanban/lists/update.html"
  form_class = ListForm
  success_url = reverse_lazy("kanban:home")

class ListDeleteView(LoginRequiredMixin, DeleteView):
  model = List
  template_name = "kanban/lists/delete.html"
  success_url = reverse_lazy("kanban:home")

class CardCreateView(LoginRequiredMixin, CreateView):
  model = Card
  template_name = "kanban/cards/create.html"
  form_class = CardForm
  success_url = reverse_lazy("kanban:home")

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "kanban/cards/list.html"


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "kanban/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
  model = Card
  template_name = "kanban/cards/update.html"
  form_class = CardForm
  success_url = reverse_lazy("kanban:home")

class CardDeleteView(LoginRequiredMixin, DeleteView):
  model = Card
  template_name = "kanban/cards/delete.html"
  success_url = reverse_lazy("kanban:home")

class HomeView(LoginRequiredMixin, ListView):
  model = List
  template_name = "kanban/home.html"


class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
  model = Card
  template_name = "kanban/cards/create.html"
  form_class = CardCreateFromHomeForm
  success_url = reverse_lazy("kanban:home")

  def form_valid(self, form):
    list_pk = self.kwargs["list_pk"]
    # リストモデルのPKが list_pk のものを取得
    # List.objects.get(pk=list_pk) との違いは、取得に失敗したときは404(Not Found)例外を送出する点
    list_instance = get_object_or_404(List, pk=list_pk)
    form.instance.list = list_instance
    form.instance.user = self.request.user
    return super().form_valid(form)
