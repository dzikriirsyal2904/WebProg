import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from AplikasiTest.models import AccountUser, Course, AttendingCourse
from AplikasiTest.signals import check_nim
from AplikasiTest.form import StudentRegisterForm
from django.http import HttpResponseNotFound

# Create your views here.
# ==================== ini course ======================
def home(request):
    #fungsi (def) nama fungsinya(home)
    return render(request, 'home.html')

def readCourse(request):
    data = Course.objects.all()[:1] #limit data (1 pcs)
    context = {'data_list': data}
    return render(request, 'course.html', context)

@csrf_protect
def createCourse(request):
    return render(request, 'home.html')

@csrf_protect
def updateCourse(request):
    return render(request, 'home.html')

@csrf_protect
def deleteCourse(request):
    try:
        data = Course.objects.filter(course_id=id)
        if User:
            data.delete()
            messages.success(request, 'Data Berhasil dihapus')
            return redirect('webapp:read-data-course')
        else:
            messages.success(request, 'Data Tidak ditemukan')
            return redirect('webapp:read-data-course')
    except:
        return redirect('webapp:read-data-course')

#============================ course =======================
#========================== Data student ===================

def readStudent(request):
    data = AccountUser.objects.all()
    context = {'data_list': data}
    return render(request, 'index.html', context)


@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            nim = form.cleaned_data.get("nim")
            email = form.cleaned_data.get("email")

            user, created = User.objects.get_or_create(username=email)
            if created:
                user.save()

            account_user = AccountUser(account_user_related_user=user, account_user_fullname=fullname,
                                       account_user_student_number=nim)
            account_user.save()

            messages.success(request, 'Data Berhasil disimpan')
            return redirect('WEBAPP:read-data-student')
    else:
        form = StudentRegisterForm()
    return render(request, 'form.html', {'form': form})



@csrf_protect
def updateStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            account_user_student_number = form.cleaned_data.get("nim")
            email = form.cleaned_data.get("email")

            if account_user_student_number:
                member.account_user_student_number = account_user_student_number
            else:
                messages.error(request, 'Account user student number is required')
                return render(request, 'form.html', {'form': form})

            user.email = email
            member.save()
            user.save()
            messages.success(request, 'Data Berhasil diupdate')
            return redirect('WEBAPP:read-data-student')
        else:
            print(form.errors)
    else:
        initial_data = {
            'fullname': user.first_name + '' + user.last_name,
            'nim': member.account_user_student_number,
            'email': user.email,
        }
        form = StudentRegisterForm(initial=initial_data)
    return render(request, 'form.html', {'form':form})


@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('WEBAPP:read-data-student')