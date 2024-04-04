import re
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import ExtractYear
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
import pandas as pd
from django.utils import timezone
from .models import Category, Book


def index(request):
    if request.session.has_key('is_logged'):
        # Data for the annual expenses chart
        yearly_expenses = Book.objects.annotate(year=ExtractYear('publisher_date')).values('year').annotate(expenses=Sum('distribution_expense')).order_by('year')
        
        yearly_expenses_list = list(yearly_expenses)
        yearly_expenses_json = json.dumps(yearly_expenses_list, cls=DjangoJSONEncoder)

        # Data for the popular publishers chart
        publishers_with_books = Book.objects.values('publisher').annotate(num_books=Count('id')).order_by('-num_books')
        top_publishers = list(publishers_with_books.filter(num_books__gt=3)[:15])
        top_publishers_count = sum(publisher['num_books'] for publisher in top_publishers)

        total_books = Book.objects.count()
        other_publisher = {'publisher': 'Other publishers', 'num_books': total_books-top_publishers_count}
        
        publishers_data = top_publishers + [other_publisher]

        popular_publishers_json = json.dumps(publishers_data, cls=DjangoJSONEncoder)

        # Data for total categories
        total_categories = Category.objects.count()

        # Data for categories with no books
        categories_with_no_books = Category.objects.annotate(num_books=Count('book')).filter(num_books=0)

        total_categories_with_no_books = categories_with_no_books.count()

        # Data for total expenses
        total_expenses_obj = Book.objects.aggregate(total=Sum('distribution_expense'))

        if not total_expenses_obj['total']:
           total_expenses = 0
        else:
            total_expenses = total_expenses_obj['total']

        return render(request,'home/index.html', {
            'total_books': total_books,
            'total_categories': total_categories,
            'total_categories_with_no_books': total_categories_with_no_books,
            'total_expenses': total_expenses,
            'yearly_expenses': yearly_expenses_json,
            'popular_publishers': popular_publishers_json
        })
    return redirect('/login')

def login(request):
    if request.session.has_key('is_logged'):
        return redirect('/')
    return render(request,'auth/login.html')

# Create your views here.
def register(request):
    if request.session.has_key('is_logged'):
        return redirect('/')
    return render(request,'auth/register.html')

def handleSignup(request):
    if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]

            # check for errors in input
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")

                    return redirect("/register")    
                except User.DoesNotExist:
                    if len(uname)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")

                        return redirect("/register")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")

                        return redirect("/register")
            
                    if pass1 != pass2:
                        messages.error(request," Password do not match, Please try again")

                        return redirect("/register")
            
            # create the user
            user = User.objects.create_user(uname, email, pass1)
            user.first_name=fname
            user.last_name=lname
            user.email = email

            user.save()
            messages.success(request," Your account has been successfully created")

            return redirect("/")
    else:
        return HttpResponse('404 - NOT FOUND ')

def handlelogin(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]

        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id 
            request.session["user_id"] = user
            messages.success(request, " Successfully logged in")

            return redirect('/')
        else:
            messages.error(request," Invalid Credentials, Please try again")  

            return redirect("/")  
        
    return HttpResponse('404-not found')

def handleLogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")

        return redirect('/')

def profile(request):
    if request.session.has_key('is_logged'):
        return render(request,'profile/profile.html')
    return redirect('/')

def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        return render(request,'profile/profile_edit.html')
    return redirect("/")

def profile_delete(request,id):
        user = get_object_or_404(User, id=id)

        del request.session['is_logged']
        del request.session["user_id"]
        logout(request)

        user.delete()

        messages.success(request, " Profile deleted")

        return redirect('/')

def profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = get_object_or_404(User, id=id)

            username = request.POST["uname"]
            first_name = request.POST.get('fname', '')
            last_name = request.POST.get('lname', '')
            email = request.POST["email"]
            password = request.POST.get('pass1', '')
            confirm_password = request.POST.get('pass2', '')

            if User.objects.filter(username=username).exclude(id=id).exists():
                messages.error(request," User already exists!")
                return redirect(f"/profile/{id}/profile_edit/") 

            if password != '':
                if password != confirm_password:
                        messages.error(request," Password do not match, Please try again")
                        return redirect(f"/profile/{id}/profile_edit/")
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.password = password

                user.save()
                return redirect("/")
            else:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email

                user.save()
                return redirect("profile/")
    return redirect("/")

def categories_table(request):
    if request.session.has_key('is_logged'):
        categories = Category.objects.annotate(num_books=Count('book'))
        return render(request,'categories/table.html', {'categories': categories})
    return redirect("/")

def categories_create(request):
    if request.session.has_key('is_logged'):
        return render(request,'categories/create.html')
    return redirect("/")

def handle_categories_create(request):
    if request.method =='POST':
            # get the post parameters
            name = request.POST["name"]

            # check for errors in input
            if request.method == 'POST':
                try:
                    category_exists = Category.objects.get(name=request.POST['name'].lower())
                    messages.error(request," Category already exists!")

                    return redirect("/categories/create")    
                except Category.DoesNotExist:
                    if len(name)>100:
                        messages.error(request," Category name must be max 100 characters, Please try again")

                        return redirect("/categories/create")
            
            category = Category.objects.create(name=name.lower())
            category.save()
            messages.success(request," The category has been successfully created")

            return redirect("/categories")
    else:
        return HttpResponse('404 - NOT FOUND ')
    
def categories_edit(request,id):
    if request.session.has_key('is_logged'):
        category = get_object_or_404(Category, id=id)

        return render(request,'categories/edit.html', {'category': category})
    return redirect("/")

def handle_categories_edit(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            category = get_object_or_404(Category, id=id)
            name = request.POST["name"]

            if Category.objects.filter(name=name.lower()).exclude(id=id).exists():
                messages.error(request," Category already exists!")
                return redirect(f"/categories/edit/{id}") 
            else:
                category.name = name.lower()
                category.save()
                messages.success(request," The category has been successfully edited")
                return redirect("/categories")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect("/")
    
def categories_delete(request,id):
    if request.session.has_key('is_logged'):
        category = get_object_or_404(Category, id=id)
        category.delete();
        
        messages.success(request," The category has been successfully deleted")
        return redirect("/categories")
    return redirect("/")

def categories_delete_all(request):
    if request.session.has_key('is_logged'):
        Category.objects.all().delete();
        
        messages.success(request," The categories have been successfully deleted")
        return redirect("/categories")
    return redirect("/")

def categories_import(request):
    if request.session.has_key('is_logged'):
        return render(request, 'categories/import.html')
    return redirect("/")

def handle_categories_import(request):
    try:
        if request.session.has_key('is_logged'):
            if request.method == 'POST':
                excel_file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                uploaded_file_path = fs.path(filename)

                empexceldata = pd.read_excel(uploaded_file_path)
                dbframe = empexceldata
                dbframe = dbframe.fillna("")

                for dbframe in dbframe.itertuples():
                    noId = False
                    cleaned_id = re.sub("[^0-9]", "", str(dbframe.id))
                    cleaned_id = int(cleaned_id)

                    if len(dbframe.name)>100:
                        continue

                    try:
                        category_exists_id = Category.objects.get(id=cleaned_id)
                        if category_exists_id:
                            noId = True
                    except Category.DoesNotExist:
                        pass

                    try:
                        category_exists_name = Category.objects.get(name=dbframe.name.lower())
                        if category_exists_name:
                            continue
                    except Category.DoesNotExist:
                        pass

                    if noId:
                        category = Category.objects.create(
                            name=dbframe.name.lower()
                        );
                        category.save();
                    else:
                        category = Category.objects.create(
                            id=cleaned_id,
                            name=dbframe.name.lower()
                        );
                        category.save();

                messages.success(request," The category data has been successfully imported")
                return JsonResponse({'success': True, 'redirect_url': '/categories/'})
            else:
                return HttpResponse('404 - NOT FOUND ')
        return redirect("/")
    except Exception as e:
        messages.error(request, " There has been an internal error in the server. Check console to know more about it.")
        return JsonResponse({'success': False, 'error': 'Internal Server Error', 'detail': str(e)}, status=500)
    finally:
        fs.delete(uploaded_file_path)

def books_table(request):
    if request.session.has_key('is_logged'):
        books = Book.objects.all();
        return render(request,'books/table.html', {'books': books})
    return redirect("/")

def books_create(request):
    if request.session.has_key('is_logged'):
        categories = Category.objects.all();
        return render(request,'books/create.html', {'categories': categories})
    return redirect("/")

def handle_books_create(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
                # get the post parameters
                title = request.POST["title"]
                subtitle = request.POST.get('subtitle', '')
                authors = request.POST.get('authors', '')
                publisher = request.POST.get('publisher', '')
                publisher_date = request.POST.get('publisher_date', None)
                category = request.POST["category"]
                distribution_expense = request.POST["distribution_expense"]

                # check for errors in input
                if request.method == 'POST':
                    try:
                        book_exists = Book.objects.get(title=request.POST['title'])
                        messages.error(request," Book already exists!")

                        return redirect("/categories/create")    
                    except Book.DoesNotExist:
                        if len(title)>100:
                            messages.error(request," Book title must be max 100 characters, Please try again")
                            return redirect("/books/create")
                    try:
                        category_obj = Category.objects.get(id=request.POST['category'])
                    except Category.DoesNotExist:
                        messages.error(request," The selected category does not exists!")
                        return redirect("/books/create")
                    
                    if publisher_date:
                        try:
                            publisher_date_obj = datetime.datetime.strptime(publisher_date, '%Y-%m-%d').date()
                        except ValueError:
                            messages.error(request, "Invalid date format for publisher date. Please use YYYY-MM-DD format.")
                            return redirect("/books/create")
                    else:
                        publisher_date_obj = None
                    
                book = Book.objects.create(
                    title=title,
                    category=category_obj,
                    distribution_expense=distribution_expense
                );
                book.subtitle=subtitle;
                book.authors=authors;
                book.publisher=publisher;
                book.publisher_date=publisher_date_obj;
                book.save();

                messages.success(request," The book has been successfully created")

                return redirect("/books")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect("/")

def books_edit(request,id):
    if request.session.has_key('is_logged'):
        book = get_object_or_404(Book, id=id)
        book.publisher_date = book.publisher_date.strftime('%Y-%m-%d')
        categories = Category.objects.all();

        return render(request,'books/edit.html', {'categories': categories, 'book':book})
    return redirect("/")

def handle_books_edit(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            book = get_object_or_404(Book, id=id)

            title = request.POST["title"]
            subtitle = request.POST.get('subtitle', '')
            authors = request.POST.get('authors', '')
            publisher = request.POST.get('publisher', '')
            publisher_date = request.POST.get('publisher_date', None)
            category = request.POST["category"]
            distribution_expense = request.POST["distribution_expense"]

            if Book.objects.filter(title=title).exclude(id=id).exists():
                messages.error(request," Book already exists!")
                return redirect(f"/books/edit/{id}") 
            else:
                try:
                    category_obj = Category.objects.get(id=category)
                except Category.DoesNotExist:
                    messages.error(request," The selected category does not exists!")
                    return redirect(f"/books/edit/{id}")
                if publisher_date:
                    try:
                        publisher_date_obj = datetime.datetime.strptime(publisher_date, '%Y-%m-%d').date()
                    except ValueError:
                        messages.error(request, "Invalid date format for publisher date. Please use YYYY-MM-DD format.")
                        return redirect(f"/books/edit/{id}")
                else:
                    publisher_date_obj = None

                if len(title)>100:
                    messages.error(request," Book title must be max 100 characters, Please try again")
                    return redirect(f"/books/edit/{id}") 

                book.title=title
                book.subtitle=subtitle;
                book.authors=authors;
                book.publisher=publisher;
                book.publisher_date=publisher_date_obj;
                book.category=category_obj
                book.distribution_expense=distribution_expense
                book.save();
                
                messages.success(request," The book has been successfully edited")
                return redirect("/books")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect("/")

def books_delete(request,id):
    if request.session.has_key('is_logged'):
        book = get_object_or_404(Book, id=id)
        book.delete();

        messages.success(request," The book has been successfully deleted")
        return redirect("/books")
    return redirect("/")

def books_delete_all(request):
    if request.session.has_key('is_logged'):
        Book.objects.all().delete();

        messages.success(request," The books have been successfully deleted")
        return redirect("/books")
    return redirect("/")

def books_import(request):
    if request.session.has_key('is_logged'):
        return render(request, 'books/import.html')
    return redirect("/")

def handle_books_import(request):
    try:
        if request.session.has_key('is_logged'):
            if request.method == 'POST':
                excel_file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                uploaded_file_path = fs.path(filename)

                empexceldata = pd.read_excel(uploaded_file_path)
                dbframe = empexceldata
                dbframe = dbframe.fillna("")

                for dbframe in dbframe.itertuples():
                    noId = False
                    cleaned_id = re.sub("[^0-9]", "", str(dbframe.id))
                    cleaned_id = int(cleaned_id)

                    if len(dbframe.title)>100:
                        continue

                    try:
                        book_exists_id = Book.objects.get(id=cleaned_id)
                        if book_exists_id:
                            noId = True
                    except Book.DoesNotExist:
                        pass

                    try:
                        book_exists_title = Book.objects.get(title=dbframe.title)
                        if book_exists_title:
                            continue
                    except Book.DoesNotExist:
                        pass
                    
                    if dbframe.published_date:
                        try:
                            publisher_date_obj = dbframe.published_date.date()
                        except ValueError:
                            continue
                    else:
                        publisher_date_obj = None

                    try:
                        category = Category.objects.get(name=dbframe.category.lower())
                    except Category.DoesNotExist:
                        category = Category.objects.create(name=dbframe.category.lower())
                        category.save()

                    if noId:
                        book = Book.objects.create(
                            title=dbframe.title,
                            category=category,
                            distribution_expense=dbframe.distribution_expense
                        );
                        book.subtitle = dbframe.subtitle;
                        book.authors = dbframe.authors;
                        book.publisher = dbframe.publisher;
                        book.publisher_date = publisher_date_obj;
                        book.save();
                    else:
                        book = Book.objects.create(
                            id=cleaned_id,
                            title=dbframe.title,
                            category=category,
                            distribution_expense=dbframe.distribution_expense
                        );
                        book.subtitle = dbframe.subtitle;
                        book.authors = dbframe.authors;
                        book.publisher = dbframe.publisher;
                        book.publisher_date = publisher_date_obj;
                        book.save();

                messages.success(request," The book data has been successfully imported")
                return JsonResponse({'success': True, 'redirect_url': '/books/'})
            else:
                return HttpResponse('404 - NOT FOUND ')
        return redirect("/")
    except Exception as e:
        messages.error(request, " There has been an internal error in the server. Check console to know more about it.")
        return JsonResponse({'success': False, 'error': 'Internal Server Error', 'detail': str(e)}, status=500)
    finally:
        fs.delete(uploaded_file_path)

def popular_categories(request):
    if request.session.has_key('is_logged'):
        top_categories = Category.objects.annotate(num_books=Count('book')).order_by('-num_books')[:10]

        top_categories_list = list(top_categories.values('name', 'num_books'))
        top_categories_json = json.dumps(top_categories_list, cls=DjangoJSONEncoder)

        return render(request, 'reports/popularCategories.html', {'top_categories': top_categories_json})
    return redirect("/")

def expenses_categories(request):
    if request.session.has_key('is_logged'):
        expenses_categories = Category.objects.annotate(total_expenses=Sum('book__distribution_expense')).order_by('-total_expenses')[:10]

        expenses_categories_list = list(expenses_categories.values('name', 'total_expenses'))

        expenses_categories_json = json.dumps(expenses_categories_list, cls=DjangoJSONEncoder)

        return render(request, 'reports/expensesCategories.html', {'expenses_categories': expenses_categories_json})
    return redirect("/")

def popular_publishers(request):
    if request.session.has_key('is_logged'):
        publishers_with_books = Book.objects.values('publisher').annotate(num_books=Count('id')).order_by('-num_books')
        top_publishers = list(publishers_with_books.filter(num_books__gt=3)[:15])
        top_publishers_count = sum(publisher['num_books'] for publisher in top_publishers)

        total_books = Book.objects.count()
        other_publisher = {'publisher': 'Other publishers', 'num_books': total_books-top_publishers_count}
        
        publishers_data = top_publishers + [other_publisher]

        popular_publishers_json = json.dumps(publishers_data, cls=DjangoJSONEncoder)

        return render(request, 'reports/popularPublishers.html', {'popular_publishers': popular_publishers_json})
    return redirect("/")

def yearly_expenses(request):
    if request.session.has_key('is_logged'):
        yearly_expenses = Book.objects.annotate(year=ExtractYear('publisher_date')).values('year').annotate(expenses=Sum('distribution_expense')).order_by('year')
        
        yearly_expenses_list = list(yearly_expenses)
        yearly_expenses_json = json.dumps(yearly_expenses_list, cls=DjangoJSONEncoder)

        return render(request, 'reports/yearlyExpenses.html', {'yearly_expenses': yearly_expenses_json})
    return redirect("/")

def custom_404(request, exception):
    return render(request, '404.html', status=404)
