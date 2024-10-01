from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import Schedule, Event
from .forms import ScheduleForm, EventForm, PasswordForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages


def home(request):
    schedules = Schedule.objects.all()

    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            # Здесь вам нужно будет связать событие с расписанием
            schedule_id = request.POST.get('schedule_id')
            schedule = Schedule.objects.get(id=schedule_id)
            event.schedule = schedule
            event.save()

            # Отправка уведомления о новом событии
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'schedule_{schedule.id}',
                {
                    'type': 'new_event',
                    'event': {
                        'time': event.time.isoformat(),
                        'place': event.place,
                        'participant_name': event.participant_name,
                    }
                }
            )
            return redirect('home')
    else:
        event_form = EventForm()

    return render(request, 'schedules/home.html', {
        'event_form': event_form,
        'schedules': schedules,
    })


def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, 'Расписание успешно создано! Не забудьте запомнить пароль.')
            return redirect('home')
    else:
        form = ScheduleForm()
    return render(request, 'schedules/create_schedule.html', {'form': form})


def schedule_detail(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    events = Event.objects.filter(schedule=schedule)

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)
        if password_form.is_valid():
            if password_form.cleaned_data['password'] == schedule.password:
                request.session['schedule_id'] = schedule_id
                return redirect('schedule_detail', schedule_id=schedule_id)
            else:
                messages.error(request, 'Неверный пароль.')

    password_form = PasswordForm()
    return render(request, 'schedules/schedule_detail.html', {
        'schedule': schedule,
        'events': events,
        'password_form': password_form,
    })


def home_view(request):
    return render(request, 'home.html')


def schedules_view():
    return render(request, 'create_schedule.html')