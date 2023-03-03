from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import reverse_lazy
urlpatterns = [
    path('', views.BookListView.as_view(), name='all'),
    # path('book/create',views.BookCreateView.as_view(success_url=reverse_lazy('all')), name='book_create'),
    path('book/create',views.bookCreate, name='book_create'),
    path('book/<int:pk>/addToMyBook',views.ReadBook.as_view(success_url=reverse_lazy('all')),name='add_to_myBook'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/update',views.BookUpdateView.as_view(success_url=reverse_lazy('all')), name='book_update'),
    path('book/<int:pk>/delete',views.BookDeleteView.as_view(success_url=reverse_lazy('all')), name='book_delete'),
    path('book/<int:pk>/read',views.BookReading.as_view(), name='book_reading'),
    path('book/<int:pk>/page',views.PageRead.as_view(), name='book_page_read'),

]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

