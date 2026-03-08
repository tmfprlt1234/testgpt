from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecordForm
from .models import Record


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            messages.success(request, '데이터가 저장되었습니다.')
            return redirect('dashboard')
    else:
        form = RecordForm()

    records = Record.objects.filter(owner=request.user)

    category = request.GET.get('category', '').strip()
    keyword = request.GET.get('q', '').strip()
    min_amount = request.GET.get('min_amount', '').strip()
    max_amount = request.GET.get('max_amount', '').strip()
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if category:
        records = records.filter(category=category)
    if keyword:
        records = records.filter(Q(title__icontains=keyword) | Q(note__icontains=keyword))
    if min_amount:
        records = records.filter(amount__gte=min_amount)
    if max_amount:
        records = records.filter(amount__lte=max_amount)

    allowed_sort = {'created_at', 'amount', 'title', 'category'}
    if sort_by not in allowed_sort:
        sort_by = 'created_at'
    if sort_order not in {'asc', 'desc'}:
        sort_order = 'desc'

    ordering = f'-{sort_by}' if sort_order == 'desc' else sort_by
    records = records.order_by(ordering)

    base_params = {}
    if category:
        base_params['category'] = category
    if keyword:
        base_params['q'] = keyword
    if min_amount:
        base_params['min_amount'] = min_amount
    if max_amount:
        base_params['max_amount'] = max_amount

    def make_sort_query(column: str) -> str:
        next_order = 'asc' if sort_by != column or sort_order == 'desc' else 'desc'
        params = {**base_params, 'sort_by': column, 'sort_order': next_order}
        return urlencode(params)

    context = {
        'form': form,
        'records': records,
        'filters': {
            'category': category,
            'q': keyword,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'sort_by': sort_by,
            'sort_order': sort_order,
        },
        'sort_links': {
            'title': make_sort_query('title'),
            'category': make_sort_query('category'),
            'amount': make_sort_query('amount'),
            'created_at': make_sort_query('created_at'),
        },
    }
    return render(request, 'records/dashboard.html', context)


@login_required
def edit_record(request, record_id):
    record = get_object_or_404(Record, id=record_id, owner=request.user)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, '데이터가 수정되었습니다.')
            return redirect('dashboard')
    else:
        form = RecordForm(instance=record)

    return render(request, 'records/edit_record.html', {'form': form, 'record': record})


@login_required
def delete_record(request, record_id):
    record = get_object_or_404(Record, id=record_id, owner=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, '데이터가 삭제되었습니다.')
    return redirect('dashboard')
