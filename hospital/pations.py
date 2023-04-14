from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re
import os
import json
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import stripe


@login_required(login_url='/login/')
def add_pations(request):
    if request.user.is_superuser == True:
        user_data = User()
        data_illness = Lillnes.objects.all()
        if 'add_pations' in request.POST:
            password = request.POST['password']
            repassword = request.POST['repassword']
            if password != repassword:
                messages.error(request, 'Password Not Match?')
                return render(request, 'add_pations.html')
            conform_password = re.search(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            if conform_password is None:
                messages.error(request, 'Password Not Valid?')
                return render(request, 'add_pations.html')
            user_data.username = request.POST['username']
            user_data.first_name = request.POST['fname']
            user_data.last_name = request.POST['lname']
            user_data.email = request.POST['email']
            user_data.phone = request.POST['phone']
            user_data.img = request.FILES['img']
            user_data.category = request.POST['category']
            user_data.set_password(password)
            selected_illness_name = request.POST['lillness']
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    user_data.lillness = i_illnes
                    user_data.save()
            messages.success(request, 'Add Pation Sucess')
            return render(request, 'base.html')
        return render(request, 'add_pations.html', {'data': data_illness})
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def view_pations(request):
    if request.user.is_superuser == True:
        pations_view_data = User.objects.filter(
            category='P', check_out_status=False).order_by('id')
        return render(request, 'view_pations.html', {'pations_data': pations_view_data})
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def update(request, id):
    if request.user.is_superuser == True:
        pation_data = User.objects.get(id=id)
        data_illness = Lillnes.objects.all()
        if 'update_pations' in request.POST:
            if len(request.FILES) != 0:
                if len(pation_data.img) > 0:
                    os.remove(pation_data.img.path)
                    pation_data.img = request.FILES['img']
            pation_data.username = request.POST['username']
            pation_data.first_name = request.POST['fname']
            pation_data.last_name = request.POST['lname']
            pation_data.email = request.POST['email']
            pation_data.phone = request.POST['phone']
            pation_data.is_active = request.POST['block']
            selected_illness_name = request.POST['lillness']
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    pation_data.lillness = i_illnes
                    pation_data.save()
            messages.success(request, 'Update Sucessfully')
            return render(request, 'base.html')
        contex = {
            'pation_data': pation_data,
            'data': data_illness
        }
        return render(request, 'add_pations.html', contex)
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def Home(request):
    if request.user.category == 'P':
        illness = request.user.lillness.lillne_id
        pation_id = request.user.id
        data_doctor = User.objects.filter(
            is_superuser=False, is_staff=True, lillness=illness).order_by('fess')
        room_data = room.objects.all()
        bed_data = bed.objects.filter(user_id=pation_id)
        user_medicine_data = ""
        if request.user.medicines != None:
            user_medicine_data = json.loads(request.user.medicines)
        if 'doc_id' in request.GET:
            selected_doctor_id = request.GET['doc_id']
            User.objects.filter(id=pation_id).update(
                doctor_id=selected_doctor_id)
            return redirect('pation-Home')
        elif 'staff_id' in request.GET:
            selected_staff_id = request.GET['staff_id']
            User.objects.filter(id=pation_id).update(
                staff_id=selected_staff_id)
            return redirect('pation-Home')
        elif request.method == 'POST':
            if request.user.doctor_id == "" or request.user.doctor_id == None:
                messages.error(request, 'Select Docotor ')
            elif request.user.staff_id == None or request.user.staff_id == "":
                messages.error(request, 'Select Staff ')
            else:
                select_room = request.POST['select_room']
                User.objects.filter(id=pation_id).update(room=select_room)
            return redirect('pation-Home')
        contex = {
            'data': data_doctor,
            'room_data': room_data,
            'bed_data': bed_data,
            'user_medicine_data': user_medicine_data
        }
        return render(request, 'pation_home.html', contex)
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def checkout(request):
    if request.user.category == 'P':
        today_obj = datetime.strptime(
            datetime.today().strftime("%Y-%m-%d"), '%Y-%m-%d')
        data_obj = datetime.strptime(
            request.user.date_joined.strftime("%Y-%m-%d"), '%Y-%m-%d')
        total_day = (today_obj - data_obj).days
        user_all = User.objects.exclude(category='P')
        room_user_data = bed.objects.get(user_id=request.user.id)
        check_out_data = {}
        email = request.user.email
        if request.user.doctor_id != None or request.user.staff_id != None:
            for Docdate in user_all:
                if Docdate.id == request.user.doctor_id:
                    check_out_data['doctor_fess'] = Docdate.fess * total_day
                elif Docdate.id == request.user.staff_id:
                    check_out_data['staff_fess'] = Docdate.fess * total_day
        if request.user.user_bed != None:
            check_out_data['room_bills'] = room_user_data.roomId.roomPrice * total_day
        if request.user.medicines != None:
            user_medicine_data = json.loads(request.user.medicines)
            check_out_data['medicine_bills'] = 0
            for i in user_medicine_data:
                check_out_data['medicine_bills'] += i['Total']
        check_out_data['Total'] = sum(check_out_data.values())
        contex = {
            'check_out_data': check_out_data,
        }
        user_data = User.objects.get(id=request.user.id)
        user_data.user_bills = check_out_data['Total']
        user_data.save()
        send_email(request, contex, email)
        return render(request, 'checkout/checkout.html', contex)
    return HttpResponseNotFound('Page Not Found')


def send_email(request, contex, email):
    html_page = render_to_string("email.html", contex)
    text_contant = strip_tags(html_page)
    fail_silently = True
    from_email = "kishansavaliya.zechrom@gmail.com"
    to = email
    msg = EmailMultiAlternatives("CheckOut", text_contant, from_email, [to])
    msg.attach_alternative(html_page, "text/html")
    msg.send()


def user_chekout(request, check_out_data):
    user_data = User.objects.get(id=request.user.id)
    user_data.user_bills = check_out_data['Total']
    user_data.save()


stripe.api_key = 'sk_test_51MKFzJSFuqhlmvOpb6j1hsW9fzdv8b0vzjYmVZlPpTO7g2Zuw2l0ZEWwoEJjvmgamFBCg52ND8R5tjVLQ9DYtApu00P1ubUcCE'


@login_required(login_url='/login/')
def create_checkout_session(request):
    if request.user.category == 'P':
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Hospital Bill Payments',
                    },
                    'unit_amount': int(request.user.user_bills) * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/check-Out/payment/success/',
            cancel_url='http://127.0.0.1:8000/check-Out/payment/cancel/',
        )
        return redirect(session.url, code=303)
    return HttpResponseNotFound('Page Not Found')


def Success(request):
    user_data = User.objects.get(id=request.user.id)
    user_data.is_active = False
    user_data.check_out_status = True
    user_data.save()
    bed.objects.filter(user_id=request.user.id).delete()
    messages.success(request, "Payment Successfull.")
    return redirect('logout')


def Cancel(request):
    messages.success(request, "Payment Faild.")
    return redirect('pation-Home')
