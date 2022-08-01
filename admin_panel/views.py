import datetime
from operator import index
from django.shortcuts import redirect, render
from admin_panel.forms import AboutUsForm, BranchForm, BrandForm, FaqForm, NewCarForm, VehicleForm
from main_site.models import FAQ, Booking, CustomerQuery, CustomerReview
from . import models
from django.contrib import auth
from user.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


# Dashboard view
@login_required
def dashboard(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()
        users = User.objects.all().filter(is_staff=False)
        new_users = 0
        for user in users:
            if user.date_joined.date() == datetime.date.today():
                new_users += 1

        booking_count = 0
        active_bookings = 0
        revenue = 0

        for booking in bookings:
            if booking.pick_up_date.date() == datetime.date.today():
                booking_count += 1
                if booking.confirmed and not booking.completed:
                    active_bookings += 1
                revenue += booking.vehicle.price

        vehicles = models.Vehicle.objects.all()
        total_no_of_vehicles = 0
        for vehicle in vehicles:
            total_no_of_vehicles += vehicle.stock

        queries = CustomerQuery.objects.all()
        pending = queries.filter(resolved=False)

        no_of_days_recorded = 7
        no_of_days_recorded_in_prev_week = 14
        revenue_list = []
        last_week_revenue_list = []
        bookings_this_week = []
        bookings_last_week = []

        for day in range(0, no_of_days_recorded, 1):
            revenue_list.append(0)
            bookings_this_week.append(0)
            for booking in bookings:
                if booking.pick_up_date.date() == datetime.date.today() - datetime.timedelta(days=day):
                    revenue_list[day] += booking.vehicle.price
                    bookings_this_week[day] += 1

        index = 0
        for day in range(7, no_of_days_recorded_in_prev_week, 1):
            last_week_revenue_list.append(0)
            bookings_last_week.append(0)
            for booking in bookings:
                if booking.pick_up_date.date() == datetime.date.today() - datetime.timedelta(days=day):
                    last_week_revenue_list[index] += booking.vehicle.price
                    bookings_last_week[index] += 1
            index += 1

        revenue_list_month = []
        last_month_revenue_list = []
        bookings_this_month = []
        bookings_last_month = []

        no_of_days_in_month_recorded = 31
        no_of_days_recorded_in_prev_month = 62

        for day in range(0, no_of_days_in_month_recorded, 1):
            revenue_list_month.append(0)
            bookings_this_month.append(0)
            for booking in bookings:
                if booking.pick_up_date.date() == datetime.date.today() - datetime.timedelta(days=day):
                    revenue_list_month[day] += booking.vehicle.price
                    bookings_this_month[day] += 1

        index_m = 0
        for day in range(31, no_of_days_recorded_in_prev_month, 1):
            last_month_revenue_list.append(0)
            bookings_last_month.append(0)
            for booking in bookings:
                if booking.pick_up_date.date() == datetime.date.today() - datetime.timedelta(days=day):
                    last_month_revenue_list[index_m] += booking.vehicle.price
                    bookings_last_month[index_m] += 1
            index_m += 1

        context = {
            'bookings': bookings,
            'users': users,
            'new_users': new_users,
            'booking_count': booking_count,
            'active_bookings': active_bookings,
            'total_no_of_vehicles': total_no_of_vehicles,
            'available_vehicles': total_no_of_vehicles - active_bookings,
            'queries': queries,
            'pending': pending,
            'revenue': revenue,
            'revenue_list': revenue_list,
            'last_week_revenue_list': last_week_revenue_list,
            'bookings_this_week': bookings_this_week,
            'bookings_last_week': bookings_last_week,
            'revenue_list_month': revenue_list_month,
            'last_month_revenue_list': last_month_revenue_list,
            'bookings_this_month': bookings_this_month,
            'bookings_last_month': bookings_last_month,
        }

        return render(request, 'admin_panel/dashboard.html', context)
    else:
        return redirect('home')


@login_required
def vehicles(request):
    if request.user.is_staff:
        brands = models.Brand.objects.all().order_by('brand_name')
        vehicles = models.Vehicle.objects.all().order_by('-id')

        context = {
            "brands": brands,
            "brandForm": BrandForm(),
            "vehicles": vehicles
        }

        return render(request, 'admin_panel/vehicles.html', context)
    else:
        return redirect('home')


@login_required
def vehicle_details(request, slug):
    if request.user.is_staff:
        vehicle = models.Vehicle.objects.get(slug=slug)

        context = {
            'vehicle': vehicle
        }
        return render(request, 'admin_panel/vehicledetails.html', context)
    else:
        return redirect('home')


@login_required
def filter_vehicle(request, slug):
    if request.user.is_staff:
        brands = models.Brand.objects.all().order_by('brand_name')
        vehicles = models.Vehicle.objects.all().filter(
            brand=models.Brand.objects.get(slug=slug)).order_by('-id')

        context = {
            "brands": brands,
            "brandForm": BrandForm(),
            "vehicles": vehicles
        }

        return render(request, 'admin_panel/vehicles.html', context)
    else:
        return redirect('home')


@login_required
def add_brand(request):
    if request.user.is_staff:
        if request.method == "POST":
            addBrandForm = BrandForm(request.POST)
            if addBrandForm.is_valid():
                addBrandForm.save()

                return redirect(request.META.get('HTTP_REFERER'))

        else:
            addBrandForm = BrandForm()

    else:
        return redirect('home')


@login_required
def edit_brand(request, slug):
    if request.user.is_staff:
        if request.method == 'POST':
            editBrandForm = BrandForm(
                request.POST or None, instance=models.Brand.objects.get(slug=slug))

            if editBrandForm.is_valid():
                editBrandForm.save()

                return redirect('vehicles')

        else:
            editBrandForm = BrandForm(
                instance=models.Brand.objects.get(slug=slug))

        context = {
            'brandForm': editBrandForm,
        }
        return render(request, 'admin_panel/editbrand.html', context)

    else:
        return redirect('home')


@login_required
def delete_brand(request, slug):
    if request.user.is_staff:
        brand = models.Brand.objects.get(slug=slug)
        brand.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def branches(request):
    if request.user.is_staff:
        branches = models.Branch.objects.all()

        no_of_days_recorded = 7
        bookings_this_week = []
        revenues_this_week = []

        index = 0
        for branch in branches:
            bookings_this_week.append(0)
            revenues_this_week.append(0)
            for day in range(0, no_of_days_recorded, 1):
                for booking in branch.bookings.all():
                    if booking.pick_up_date.date() == datetime.date.today() - datetime.timedelta(days=day):
                        bookings_this_week[index] += 1
                        revenues_this_week[index] += booking.vehicle.price
            index += 1

        context = {
            'branches': branches,
            'branchForm': BranchForm(),
            'bookings_this_week': bookings_this_week,
            'revenues_this_week': revenues_this_week,
        }

        return render(request, 'admin_panel/branches.html', context)
    else:
        return redirect('home')


@login_required
def add_branch(request):
    if request.user.is_staff:
        if request.method == "POST":
            addBranchForm = BranchForm(request.POST)
            if addBranchForm.is_valid():
                addBranchForm.save()

                return redirect(request.META.get('HTTP_REFERER'))

        else:
            addBranchForm = BrandForm()

    else:
        return redirect('home')


@login_required
def edit_branch(request, slug):
    if request.user.is_staff:
        if request.method == 'POST':
            editBranchForm = BranchForm(
                request.POST or None, instance=models.Branch.objects.get(slug=slug))

            if editBranchForm.is_valid():
                editBranchForm.save()

                return redirect('branches')

        else:
            editBranchForm = BranchForm(
                instance=models.Branch.objects.get(slug=slug))

        context = {
            'branchForm': editBranchForm,
        }
        return render(request, 'admin_panel/editbranch.html', context)

    else:
        return redirect('home')


@login_required
def delete_branch(request, slug):
    if request.user.is_staff:
        branch = models.Branch.objects.get(slug=slug)
        branch.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def add_vehicle(request):
    if request.user.is_staff:
        if request.method == 'POST':
            vehicle_form = VehicleForm(request.POST, request.FILES)

            if vehicle_form.is_valid():
                vehicle_form.save()

                return redirect('vehicles')

        else:
            vehicle_form = VehicleForm()
        context = {
            "vehicle_form": vehicle_form
        }

        return render(request, 'admin_panel/vehicleform.html', context)
    else:
        return redirect('home')


@login_required
def edit_vehicle(request, slug):
    if request.user.is_staff:
        vehicle = models.Vehicle.objects.get(slug=slug)
        if request.method == 'POST':
            vehicle_form = VehicleForm(
                request.POST or None, request.FILES or None, instance=vehicle)

            if vehicle_form.is_valid():
                vehicle_form.save()

                return redirect('vehicles')

        else:
            vehicle_form = VehicleForm(
                instance=vehicle)
        context = {
            "vehicle_form": vehicle_form,
            "vehicle": vehicle
        }

        return render(request, 'admin_panel/vehicleform.html', context)
    else:
        return redirect('home')


@login_required
def delete_vehicle(request, slug):
    if request.user.is_staff:
        vehicle = models.Vehicle.objects.get(slug=slug)
        vehicle.delete()

        return redirect('vehicles')
    else:
        return redirect('home')


@login_required
def show_comment_in_website(request, id):
    if request.user.is_staff:
        comment = models.VehicleComment.objects.get(id=id)
        comment.should_show = not comment.should_show
        comment.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def delete_comment(request, id):
    if request.user.is_staff:
        comment = models.VehicleComment.objects.get(id=id)
        comment.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def registered_users(request):
    if request.user.is_staff:
        users = User.objects.all().filter(is_staff=False).order_by("-last_login")

        context = {
            'users': users,
        }

        return render(request, 'admin_panel/user_list.html', context)
    else:
        return redirect('home')


@login_required
def delete_user(request, id):
    if request.user.is_staff:
        user = User.objects.get(id=id)
        user.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def bookings(request):
    if request.user.is_staff:
        bookings = Booking.objects.all().order_by('-id')

        context = {
            'bookings': bookings,
        }

        return render(request, 'admin_panel/bookings.html', context)
    else:
        return redirect('home')


@login_required
def confirm_booking(request, id):
    if request.user.is_staff:
        bookings = Booking.objects.get(id=id)

        bookings.confirmed = True
        bookings.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def cancel_booking(request, id):
    if request.user.is_staff:
        bookings = Booking.objects.get(id=id)

        bookings.confirmed = False
        bookings.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def complete_booking(request, id):
    if request.user.is_staff:
        bookings = Booking.objects.get(id=id)

        bookings.completed = not bookings.completed
        bookings.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def delete_booking(request, id):
    if request.user.is_staff:
        booking = Booking.objects.get(id=id)
        booking.delete()

        return redirect('bookings')
    else:
        return redirect('home')


@login_required
def booking_details(request, id):
    if request.user.is_staff:
        bookings = Booking.objects.all().order_by('-id')
        booking = Booking.objects.get(id=id)

        context = {
            'bookings': bookings,
            'booking': booking,
        }

        return render(request, 'admin_panel/booking_details.html', context)
    else:
        return redirect('home')


@login_required
def manage_queries(request):
    if request.user.is_staff:
        queries = CustomerQuery.objects.all()
        context = {
            'queries': queries,
        }

        return render(request, 'admin_panel/manage_queries.html', context)
    else:
        return redirect('home')


@login_required
def resolved_queries(request, id):
    if request.user.is_staff:
        query = CustomerQuery.objects.get(id=id)
        query.resolved = True
        query.save()

        return redirect('manage_queries')
    else:
        return redirect('home')


@login_required
def manage_site(request):
    if request.user.is_staff:
        new_cars = models.NewCar.objects.all()
        vehicles = models.Vehicle.objects.all()
        about_details = models.AboutUs.objects.all()
        addAboutUsForm = AboutUsForm()
        editAboutUsForm = AboutUsForm()
        reviews = CustomerReview.objects.all()
        faqs = FAQ.objects.all()
        queries = CustomerQuery.objects.all()

        context = {
            'new_cars': new_cars,
            'vehicles': vehicles,
            'about_details': about_details,
            'addAboutUsForm': addAboutUsForm,
            'editAboutUsForm': editAboutUsForm,
            'reviews': reviews,
            'faqs': faqs,
            'queries': queries,
        }
        return render(request, 'admin_panel/manage_site.html', context)
    else:
        return redirect('home')


@login_required
def add_new_car(request, slug):
    if request.user.is_staff:
        new_car_form = NewCarForm(request.POST)
        if new_car_form.is_valid():
            new_car = new_car_form.save(commit=False)
            new_car.vehicle = models.Vehicle.objects.get(slug=slug)
            new_car.save()

            return redirect('manage_site')

    else:
        return redirect('home')


@login_required
def remove_new_car(request, id):
    if request.user.is_staff:
        new_car = models.NewCar.objects.get(id=id)
        new_car.delete()

        return redirect('manage_site')
    else:
        return redirect('home')


@login_required
def add_about_us(request):
    if request.user.is_staff:
        if models.AboutUs.objects.all().count() == 0 or None:
            addAboutUsForm = AboutUsForm(request.POST)

            if addAboutUsForm.is_valid():
                addAboutUsForm.save()

                return redirect('manage_site')

        else:
            return redirect('manage_site')

    else:
        return redirect('home')


@login_required
def edit_about_us(request, id):
    if request.user.is_staff:
        editAboutUsForm = AboutUsForm(
            request.POST or None, instance=models.AboutUs.objects.get(id=id))

        if editAboutUsForm.is_valid():
            editAboutUsForm.save()

            return redirect('manage_site')

    else:
        return redirect('home')


@login_required
def show_review(request, id):
    if request.user.is_staff:
        review = CustomerReview.objects.get(id=id)
        review.is_active = not review.is_active
        review.save()
        return redirect('manage_site')
    else:
        return redirect('home')


@login_required
def delete_review(request, id):
    if request.user.is_staff:
        review = CustomerReview.objects.get(id=id)
        review.delete()

        return redirect('manage_site')
    else:
        return redirect('home')


@login_required
def add_faq(request, id):
    if request.user.is_staff:
        query = CustomerQuery.objects.get(id=id)
        if request.method == 'POST':
            faqForm = FaqForm(request.POST)

            if faqForm.is_valid():
                faq = faqForm.save(commit=False)
                faq.query = query
                faq.save()
                return redirect('manage_site')
        else:
            faqForm = FaqForm()

        context = {
            'faqForm': faqForm,
            'query': query,
        }
        return render(request, 'admin_panel/faq_form.html', context)
    else:
        return redirect('home')


@login_required
def edit_faq(request, id):
    if request.user.is_staff:
        faq = FAQ.objects.get(id=id)
        query = faq.query
        if request.method == 'POST':
            faqForm = FaqForm(request.POST or None, instance=faq)

            if faqForm.is_valid():
                faq = faqForm.save(commit=False)
                faq.query = query
                faq.save()
                return redirect('manage_site')
        else:
            faqForm = FaqForm(instance=faq)

        context = {
            'faqForm': faqForm,
            'query': query,
        }
        return render(request, 'admin_panel/faq_form.html', context)
    else:
        return redirect('home')


@login_required
def delete_faq(request, id):
    if request.user.is_staff:
        faq = FAQ.objects.get(id=id)
        faq.delete()

        return redirect('manage_site')
    else:
        return redirect('home')
