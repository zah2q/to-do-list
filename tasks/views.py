# tasks/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from .models import Task

class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        self.filter_type = self.request.GET.get('filter', 'incomplete')
        if self.filter_type == 'completed':
            queryset = queryset.filter(completed=True)
        elif self.filter_type == 'today':
            # --- تم التعديل هنا: نستخدم `expiration_date` ---
            queryset = queryset.filter(expiration_date__date=timezone.now().date(), completed=False)
        elif self.filter_type == 'week':
            today = timezone.now().date()
            end_of_week = today + timezone.timedelta(days=7)
            # --- تم التعديل هنا: نستخدم `expiration_date` ---
            queryset = queryset.filter(expiration_date__date__range=[today, end_of_week], completed=False)
        elif self.filter_type == 'all':
            pass
        else: 
            queryset = queryset.filter(completed=False)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        sort_by = self.request.GET.get('sort')
        if sort_by == 'priority':
            queryset = queryset.annotate(
                priority_order=Case(
                    When(priority='H', then=Value(3)),
                    When(priority='M', then=Value(2)),
                    When(priority='L', then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            # --- تم التعديل هنا: نستخدم `expiration_date` للترتيب الثانوي ---
            ).order_by('-priority_order', 'expiration_date')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_titles = {
            'incomplete': 'المهام غير المنجزة', 'completed': 'المهام المنجزة',
            'today': 'مهام اليوم', 'week': 'مهام الأسبوع', 'all': 'كل المهام'
        }
        context['page_title'] = page_titles.get(self.filter_type, 'قائمة المهام')
        if self.request.GET.get('q'):
            context['page_title'] = f"نتائج البحث عن: '{self.request.GET.get('q')}'"
        return context

class TaskCreate(CreateView):
    model = Task
    # --- تم التعديل هنا: الحقول التي ستظهر في نموذج الإنشاء ---
    fields = ['title', 'description', 'priority', 'expiration_date', 'image']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'إضافة مهمة جديدة'
        return context

class TaskUpdate(UpdateView):
    model = Task
    # --- تم التعديل هنا: الحقول التي ستظهر في نموذج التعديل ---
    fields = ['title', 'description', 'priority', 'expiration_date', 'completed', 'image']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'تعديل مهمة: {self.object.title}'
        return context

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'tasks/task_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'حذف مهمة: {self.object.title}'
        return context

def statistics_view(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    incomplete_tasks = total_tasks - completed_tasks
    # --- تم التعديل هنا: نستخدم `expiration_date` ---
    oldest_incomplete_task = Task.objects.filter(completed=False, expiration_date__gte=timezone.now()).order_by('expiration_date').first()
    context = {
        'page_title': 'إحصائيات المهام', 'total_tasks': total_tasks,
        'completed_tasks': completed_tasks, 'incomplete_tasks': incomplete_tasks,
        'oldest_incomplete_task': oldest_incomplete_task
    }
    return render(request, 'tasks/statistics.html', context)

def toggle_task_complete(request, pk):
    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=pk)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'status': 'ok', 'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)