from django.shortcuts import render
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ==============================
    # DASHBOARDS
    # ==============================

    path(
        '',
        views.dashboard_redirect,
        name='dashboard_redirect'
    ),

    path(
        'dashboard/staff/',
        views.staff_dashboard,
        name='staff_dashboard'
    ),

    path(
        'superadmin/',
        views.superadmin_dashboard,
        name='superadmin_dashboard'
    ),


    # ==============================
    # STAFF ENTRY
    # ==============================

    path(
        'entry/staff/',
        views.staff_entry,
        name='staff_entry'
    ),

    path(
        'entry/customer/',
        views.customer_staff_entry,
        name='customer_staff_entry'
    ),


    # ==============================
    # VIEW ENTRIES
    # ==============================

    path(
        'entries/staff/',
        views.staff_entries,
        name='staff_entries'
    ),

    path(
        'entries/customer/',
        views.customer_entries,
        name='customer_entries'
    ),


    # ==============================
    # EDIT STAFF ENTRY
    # ==============================

    path(
        'entry/staff/<int:entry_id>/edit/',
        views.edit_staff_entry,
        name='edit_staff_entry'
    ),


    # ==============================
    # EXPORT EXCEL
    # ==============================

    path(
        'export/staff/',
        views.export_staff_entries,
        name='export_staff_entries'
    ),

    path(
        'export/customer/',
        views.export_customer_entries,
        name='export_customer_entries'
    ),


    # ==============================
    # EXPORT PDF
    # ==============================

    path(
        'export/staff/pdf/',
        views.export_staff_entries_pdf,
        name='export_staff_entries_pdf'
    ),

    path(
        'export/customer/pdf/',
        views.export_customer_entries_pdf,
        name='export_customer_entries_pdf'
    ),


    # ==============================
    # LOGIN / LOGOUT
    # ==============================

    path(
        'login/',
        views.custom_login,
        name='custom_login'
    ),

    path(
        'logout/',
        views.custom_logout,
        name='custom_logout'
    ),


    # ==============================
    # FORBIDDEN
    # ==============================

    path(
        'forbidden/',
        lambda request: render(
            request,
            'forbidden.html'
        ),
        name='forbidden'
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )