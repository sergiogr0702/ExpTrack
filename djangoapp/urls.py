from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/',views.register,name='register'),
    path('handlesignup/',views.handleSignup,name='handlesignup'),
    path('login/',views.login,name='login'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handleLogout,name='logout'),

    path('profile/',views.profile,name = 'profile'),
    path('profile/<int:id>/profile_edit/',views.profile_edit,name="profile_edit"),
    path('profile/<int:id>/profile_update/',views.profile_update,name="profile_update"),
    
    path('categories/',views.categories_table,name='categories'),
    path('categories/create/',views.categories_create,name='categories_create'),
    path('categories/create/handleCreate/',views.handle_categories_create,name='handle_categories_create'),
    path('categories/edit/<int:id>/',views.categories_edit,name='categories_edit'),
    path('categories/edit/<int:id>/handleEdit/',views.handle_categories_edit,name='handle_categories_edit'),
    path('categories/delete/<int:id>/',views.categories_delete,name="categories_delete"),
    path('categories/deleteAll/',views.categories_delete_all,name="categories_delete_all"),
    path('categories/import/',views.categories_import,name='categories_import'),
    path('categories/import/handleImport/',views.handle_categories_import,name='handle_categories_import'),

    path('books/',views.books_table,name='books'),
    path('books/create/',views.books_create,name='books_create'),
    path('books/create/handleCreate/',views.handle_books_create,name='handle_books_create'),
    path('books/edit/<int:id>/',views.books_edit,name='books_edit'),
    path('books/edit/<int:id>/handleEdit/',views.handle_books_edit,name='handle_books_edit'),
    path('books/delete/<int:id>/',views.books_delete,name="books_delete"),
    path('books/deleteAll/',views.books_delete_all,name="books_delete_all"),
    path('books/import/',views.books_import,name='books_import'),
    path('books/import/handleImport/',views.handle_books_import,name='handle_books_import'),

    path('reports/popularCategories/',views.popular_categories,name='popular_categories'),
    path('reports/expensesCategories/',views.expenses_categories,name='expenses_categories'),
    path('reports/popularPublishers/',views.popular_publishers,name='popular_publishers'),
    path('reports/yearlyExpenses/',views.yearly_expenses,name='yearly_expenses'),
]
