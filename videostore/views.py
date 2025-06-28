# views.py
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import GameData
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login
import pytz
from django.db.models import Max
from openpyxl.drawing.image import Image as ExcelImage
import os
from django.urls import reverse
from django.http import JsonResponse

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(staff_entry) 
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def generate_bill_no():
    india_tz = pytz.timezone("Asia/Kolkata")
    now = timezone.now().astimezone(india_tz)
    today_str = now.strftime("%d%m%y")  

    # Get the latest bill_no starting with today’s date
    last_bill = GameData.objects.filter(bill_no__startswith=today_str).aggregate(Max('bill_no'))['bill_no__max']

    if last_bill:
        last_seq = int(last_bill[-3:])  # get last 3 digits
        next_seq = f"{last_seq + 1:03d}"
    else:
        next_seq = "001"

    return today_str + next_seq

def export_report(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Game Report'

    # Headers
    headers = [
        'Staff', 'Customer ID', 'Customer Name', 'Machine', 'In Points',
        'Out Points', 'Amount', 'Expense Type', 'Bill No', 'Date', 'Time', 'Photo'
    ]
    sheet.append(headers)

    for idx, entry in enumerate(GameData.objects.all(), start=2):
        sheet.append([
            entry.staff.username,
            entry.customer_id,
            entry.customer_name,
            f"{entry.machine_name} ({entry.machine_number})",
            entry.in_points,
            entry.out_points,
            entry.good_luck,
            entry.expense_type,
            entry.bill_no,
            entry.date.strftime('%Y-%m-%d'),
            entry.time.strftime('%H:%M:%S'),
            "", 
        ])

        # Insert image correctly
        if entry.photo and os.path.exists(entry.photo.path):
            img = ExcelImage(entry.photo.path) 
            img.width = 100
            img.height = 100
            img.anchor = f"L{idx}" 
            sheet.add_image(img)

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report_with_photos.xlsx'
    workbook.save(response)
    return response

import base64
from django.core.files.base import ContentFile
IST = pytz.timezone('Asia/Kolkata')
@login_required
def staff_entry(request):
    india_tz = pytz.timezone("Asia/Kolkata")
    now = timezone.now().astimezone(india_tz)

    if request.method == 'POST':
        entry_id = request.POST.get("entry_id")
        photo_file = None
        photo_data = request.POST.get('photo_data')
        if photo_data:
            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            photo_file = ContentFile(base64.b64decode(imgstr), name=f"{random.randint(100000,999999)}.{ext}")

        if entry_id:
            # Editing existing record
            entry = GameData.objects.get(pk=entry_id)
            entry.customer_name = request.POST['customer_name']
            entry.machine_name = request.POST['machine_name']
            entry.machine_number = request.POST['machine_number']
            entry.in_points = request.POST['in_points']
            entry.out_points = request.POST['out_points']
            entry.good_luck = request.POST.get('amount') or 0
            entry.expense_type = request.POST['expense_type']
            entry.remarks = request.POST['remarks']
            entry.date = now.date()
            entry.time = now.time()
            if photo_file:
                entry.photo = photo_file
            entry.save()
        else:
            # Creating new record
            entry = GameData.objects.create(
                staff=request.user,
                customer_id="cust-" + str(random.randint(10000, 99999)),
                customer_name=request.POST['customer_name'],
                machine_name=request.POST['machine_name'],
                machine_number=request.POST['machine_number'],
                in_points=request.POST['in_points'],
                out_points=request.POST['out_points'],
                good_luck=request.POST.get('amount') or 0,
                expense_type=request.POST['expense_type'],
                bill_no=generate_bill_no(),
                photo=photo_file,
                remarks=request.POST['remarks'],
                date=now.date(),
                time=now.time(),
            )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'id': entry.id})

        messages.success(request, "✅ Data saved successfully!")
        return redirect('staff_entry')

    context = {
        'now': now,
        'customer_id': "cust-" + str(random.randint(10000, 99999)),
        'bill_no': generate_bill_no(),
    }
    return render(request, 'staff_entry.html', context)

@login_required
def all_entries(request):
    entries = GameData.objects.order_by('-id')[:100]  
    return render(request, 'entries_list.html', {'entries': entries})

