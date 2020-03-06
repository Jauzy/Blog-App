from django.shortcuts import render
from .models import Post
from django.views.generic import ( 
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Post
    #default template_name is <app>/<model>_<viewtype>.html
    #but overhere we override it
    template_name = 'blog/home.html' 
    #object name passed to html that fetch data from Post model 
    context_object_name = 'posts'
    #order by date posted descending 
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    #in this section we used this <app>/<model>_<viewtype>.html
    #so no need to specify template_name
    #object name passed to html is "object" because we dont specify it in context_object_name

#loginrequiredmixins is user need to login to access this page
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #expected template is post_form by default
    def form_valid(self, form):
        #set author of new post to current logged user
        form.instance.author = self.request.user
        return super().form_valid(form)

#loginrequiredmixins is user need to login to access this page
#userpassedtestmixins is for making certain condition for user
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    #expected template is post_form by default
    def form_valid(self, form):
        #set author of new post to current logged user
        form.instance.author = self.request.user
        return super().form_valid(form)

    #defining test condition how user can update post
    #here we define that user who created the post only can edit the post
    def test_func(self):
        #get post that gonna be updated
        post = self.get_object()
        #self.request.user get current logged user
        if self.request.user == post.author:
            return True
        return False

#loginrequiredmixins is user need to login to access this page
#userpassedtestmixins is for making certain condition for user
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    #expected template is post_confirm_delete by default
    #defining test condition how user can update post
    #here we define that user who created the post only can edit the post
    def test_func(self):
        #get post that gonna be updated
        post = self.get_object()
        #self.request.user get current logged user
        if self.request.user == post.author:
            return True
        return False

#below is function based view that we no longer use

# Create your views here.
def home(request):
    #dictionary to dummy data
    context = {
        'posts' : Post.objects.all()
    }
    #context was data passed to html
    return render(request, 'blog/home.html', context)

def about(request):
    context = {
        'title' : 'About'
    }
    return render(request, 'blog/about.html', context)


