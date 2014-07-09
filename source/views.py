from django.shortcuts import render, get_object_or_404
from source.models import Post

def index(request):
	# Get Published Posts
	post  = Post.objects.filter(published=True)


	return render(request,'source/index.html',{'post':post})

def post(request,slug):
	#get post object 
	post = get_object_or_404(Post, slug=slug)

	return render(request,'source/post.html',{'post',post})
