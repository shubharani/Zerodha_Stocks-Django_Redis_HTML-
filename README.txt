---
Requriments:

 python -3.7.3
 Django-3.1.7
 vue-
 

Create virtual python environment and installation:

1. python -m pip install --user virtualenv
2. python -m venv(or virtualenv) env
3. \env\Scripts\activate


1. pip install django
2. django-admin startproject "project_name"
3. cd project_name 
4. python manage.py migrate
5 run "python manage.py runserver"(test the django server)
#Create the Vue app
6.python manage.py startapp vue_app 
#Register the vue_app app with the mysite project

#add path to project_name/settings.py
'vue_app.apps.VueAppConfig',

#create test.html in vue_app/templates/vue_app/ :

#Open vue_app/views.py (it should already exist):

def test_vue(request):
    return render(request, 'vue_app/test.html')


#open mysite/mysite/urls.py. We’ll just define this URL globally, since it’s the only one in our test app for now.


#adding css to html 

create css in vue_app/static/ :

add path in project_name/setting.py.

#for develpment:
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'/static/'),
]


#for production:
STATIC_URL = '/static/'
STATIC_ROOT= [
    os.path.join(BASE_DIR,'/static/'),
]


add link path in html

{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'stylesheet.css' %}">

not verifed
https://riptutorial.com/redis/example/29962/installing-and-running-redis-server-on-windows

 pip install django djangorestframework redis

https://stackabuse.com/working-with-redis-in-python-with-django/