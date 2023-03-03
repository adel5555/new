from .models import Book,Pages,Reading
from django.urls import reverse_lazy
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views import View
from django.http import HttpResponseRedirect,HttpRequest,Http404
from .forms import Bookform
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import math
from django.contrib.auth.mixins import LoginRequiredMixin
class BookListView(OwnerListView,LoginRequiredMixin):
    model = Book
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_book'] = Reading.objects.filter(Reader_id=self.request.user.id)
        mybooks = list(Reading.objects.filter(Reader= self.request.user.id))
        mybooks = [item.Book.id for item in mybooks]
        context["mybookids"] = mybooks
        context["book_search"]=Book.objects.filter(name=self.request.GET.get('bookName'))
        return context
    
    


class BookDetailView(OwnerDetailView):
    model = Book
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pages"] = Pages.objects.filter(book=self.kwargs['pk'])
        context["I_have_book"] = Reading.objects.filter(Book=self.kwargs['pk'],Reader=self.request.user.id)#.order_by('page_number')
        return context

@login_required
def bookCreate(request):
    form = Bookform
    if request.method == 'POST':
        form = Bookform(request.POST)
        if form.is_valid():
            try:
                book = request.FILES['text_book'].readlines()
                form.save(commit=False)
                form.instance.author = request.user
                form.instance.MaxPageNumber = math.ceil(len(book)/50)
                form.save()
                bookID = Book.objects.latest('id')
                page_content=""
                line_counter =0
                page_counter =1
                for i in book:
                    page_content+=str(i.decode())
                    line_counter+=1
                    if(line_counter>50):
                        newpage = Pages.objects.create(book=bookID,page_number=page_counter,content=page_content)
                        newpage.save()
                        page_counter+=1
                        line_counter=0
                        page_content=""
                if page_content != "":
                    newPage = Pages(book=bookID,page_number=page_counter,content=page_content)
                    newPage.save()
            finally:
                return HttpResponseRedirect(reverse_lazy('all'))
    context = {'form':form}
    return render(request,'book/book_form.html',context)

class BookCreateView(OwnerCreateView):#TODO
    model = Book
    fields = ['name', 'MaxPageNumber','text_book']

    def get(self, request: HttpRequest, *args: str, **kwargs):
        if self.request.user.role.upper() == "READER":
            raise Http404
        else:
            return super(OwnerCreateView,self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        if self.request.user.role.upper() == "AUTHOR":
            print('form_valid called')
            object = form.save(commit=False)
            object.author = self.request.user
            # newBook = Book(name=object.name,author=self.request.user,MaxPageNumber=10)
            # newBook.save()
            object.save()
        bookID = Book.objects.latest('id')
        book = self.request.FILES['text_book'].readlines()
        page_content=""
        line_counter =0
        page_counter =1
        for i in book:
            page_content+=str(i.decode())
            line_counter+=1
            if(line_counter>50):
                newpage = Pages.objects.create(book=bookID,page_number=page_counter,content=page_content)
                newpage.save()
                page_counter+=1
                line_counter=0
                page_content=""
        if page_content != "":
            newPage = Pages(book=bookID,page_number=page_counter,content=page_content)
            newPage.save()

            
        return super(BookCreateView,self).form_valid(form)  
    
class BookUpdateView(OwnerUpdateView):
    model = Book
    fields = ['name', 'MaxPageNumber']


class BookDeleteView(OwnerDeleteView):
    model = Book


class ReadBook(OwnerCreateView):
    model = Reading
    template_name = 'book/book_read.html'
    fields=[]
    # def get_form_kwargs(self):
    #     kwargs = super(ReadBook,self).get_form_kwargs()
    #     kwargs['pk'] = self.kwargs.get('pk')
    #     return kwargs

    def get(self, request: HttpRequest, *args: str, **kwargs):
        list_my_book=Reading.objects.filter(Book_id=self.kwargs['pk'],Reader_id=self.request.user.id)
        if self.request.user.role.upper() == "AUTHOR" :
            raise Http404
        elif len(list_my_book)!=0:
            return HttpResponseRedirect(reverse_lazy("all"))
        else:
            return super(OwnerCreateView,self).get(request, *args, **kwargs)

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.Reader_id = self.request.user.id
        object.Book_id = self.kwargs['pk']
        object.save()
        return super(OwnerCreateView, self).form_valid(form)  

    

class BookReading(OwnerDetailView):
    model=Book
    template_name = 'book/book_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pages"] = Pages.objects.filter(book=self.kwargs['pk'])
        context["I_have_book"] = Reading.objects.filter(Book=self.kwargs['pk'],Reader=self.request.user.id)#.order_by('page_number')
        return context
    
class PageRead(OwnerDetailView):
    model = Pages
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = list(context["pages"].content.split(","))
        return context
    def get(self, request: HttpRequest, *args, **kwargs):
        newReadingPage = Pages.objects.get(id=self.kwargs['pk'])
        update_reading = Reading.objects.get(Reader= self.request.user.id,Book=newReadingPage.book)
        update_reading.continue_reading_from_this_page = newReadingPage.page_number
        update_reading.save()
        #newReading.continue_reading_from_this_page = self.request
        return super().get(request, *args, **kwargs)
    


class HomePage(View):
    def get_queryset(self):
        return super().get_queryset()
    
    
    