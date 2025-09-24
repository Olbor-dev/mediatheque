from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from mediatheque.forms import MediaForm, MemberForm, BorrowForm
from mediatheque.models import Media, Member, Borrow


def index(request):
    return render(request, 'index.html')

def medias(request):
    if request.method == "POST":
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medias')
    else:
        form = MediaForm()
    context = {
        'form': form,
        'medias': Media.objects.order_by('title')
    }
    return render(request, 'medias.html', context)

def members(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members')
    else:
        form = MemberForm()
    context = {
        'form': form,
        'members': Member.objects.order_by('lastname', 'firstname'),
    }
    return render(request, 'members.html', context)

def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("members")
    else:
        form = MemberForm(instance=member)
    return render(request, "member_edit.html", {"form": form, "member": member})

def borrows(request):
    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("borrows")
    else:
        form = BorrowForm()
    ongoing_borrows = Borrow.objects.filter(return_date__isnull=True)
    context = {
        'form': form,
        'borrows': ongoing_borrows.order_by('media__title') }
    return render(request, 'borrows.html', context)

def return_borrow(request,borrow_id):
    borrow = get_object_or_404(Borrow, pk=borrow_id)
    borrow.return_date = timezone.now().date()  # date du jour
    borrow.save()
    return redirect('borrows')  # redirige vers la liste des emprunts