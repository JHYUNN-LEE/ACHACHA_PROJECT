from re import search
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Posts, UserDeal
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from all_search.views import all_detail

# Create your views here.

def index(request):
    lost_items_list = Posts.objects.all().order_by('-posts_id_pk')
    # print(lost_items_list)

    paginator = Paginator(lost_items_list, 5)
    page = request.GET.get('page')

    posts = paginator.get_page(page)
    print(posts)
    print(request.user.username)
    print(request.user.id)
    return render(request, 'acha_money/acha_money.html', {'lost_items_list': lost_items_list,
                                                          'posts': posts})


def post(request):
    if request.method == 'POST':
        # posts table
        posts = Posts()
        posts.title = request.POST['title']
        posts.category = request.POST['category']
        posts.cost = request.POST['cost']
        # 이미지 파일이 없을 경우 None으로 받음
        try:
            posts.img_src = request.FILES['img_src']
        except:
            posts.img_src = None
        
        posts.content = request.POST['content']
        posts.parcel = request.POST['parcel']
        posts.created_at = timezone.now()
        posts.get_place = request.POST['get_place']
        posts.users_id = request.user
        posts.save()

        # userdeal table
        user_deal = UserDeal()
        user_deal.users_id = request.user
        user_deal.posts_id = posts.posts_id_pk
        user_deal.deal = request.POST.get('deal', '')
        user_deal.save()
        return redirect('acha_money')
    else:
        return render(request, 'acha_money/post.html')
    # data = Model.objects.create(title=title, ...)

def post_search(request, posts_id_pk):
    if request.method == 'POST':
        # posts table
        title = request.POST['title']
        category = request.POST['category']
        cost = request.POST['cost']
        # 이미지 파일이 없을 경우 None으로 받음
        try:
            img_src = request.FILES['img_src']
        except:
            img_src = None
        
        content = request.POST['content']
        parcel = request.POST['parcel']
        created_at = timezone.now()
        get_place = request.POST['get_place']
        posts = Posts.objects.filter(posts_id_pk=posts_id_pk)
        posts.update(title=title,
                    category=category,
                    cost=cost,
                    img_src=img_src,
                    content=content,
                    parcel=parcel,
                    created_at=created_at,
                    get_place=get_place,
                    users_id = request.user
                    )
        
        # userdeal table
        user_deal = UserDeal()
        user_deal.users_id = request.user
        user_deal.posts_id = posts_id_pk
        user_deal.deal = request.POST.get('deal', '')
        user_deal.save()
        return redirect('acha_money')
    else:
        search_item = Posts.objects.filter(posts_id_pk=posts_id_pk)
        return render(request, 'acha_money/post_search.html', {'search_item':search_item})
    # data = Model.objects.create(title=title, ...)



def detail(request, posts_id_pk):
    if request.method ==  'POST':
        # user_detail table
        user_deal = UserDeal()
        user_deal.users_id = request.user
        user_deal.posts_id = posts_id_pk
        user_deal.deal = request.POST.get('deal', '')
        user_deal.save()
        return redirect('acha_money')
        
    else:
        detail = Posts.objects.filter(posts_id_pk=posts_id_pk)
        print(detail)
        
        
        # if detail.users_id == request.user:
            # detail = True
        # else:
            # detail = False
        return render(request, 'acha_money/post_detail.html', {'detail': detail})


def result(request):
    return render(request, 'acha_money/test_result.html')

def delete(request, posts_id_pk):
    post = Posts.objects.get(posts_id_pk=posts_id_pk).delete()
    # if  post.users_id == request.user:
    print(post)
    # test = post.delete()
    # print(test)
    return redirect('acha_money')
    # else:
        # return redirect(f'acha_money/detail/{posts_id_pk}/')
        
        
def update(request, posts_id_pk):
    if request.method == "POST":
        title = request.POST['title']
        category = request.POST['category']
        cost = request.POST['cost']
        # 이미지 파일이 없을 경우 None으로 받음
        try:
            img_src = request.FILES['img_src']
        except:
            img_src = None
        content = request.POST['content']
        parcel = request.POST['parcel']
        created_at = timezone.now()
        get_place = request.POST['get_place']
        
        posts = Posts.objects.filter(posts_id_pk=posts_id_pk)
        
        posts.update(title=title,
                     category=category,
                     cost=cost,
                     img_src=img_src,
                     content=content,
                     parcel=parcel,
                     created_at=created_at,
                     get_place=get_place)
        return redirect('acha_money')
    else:
        posts = Posts.objects.get(posts_id_pk=posts_id_pk)
        return render(request, 'acha_money/update.html', {'posts':posts})