from django.shortcuts import render, get_object_or_404, redirect
from .models import DevTool
from .forms import DevToolForm

# 개발툴 리스트
def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'devtools/devtool_list.html', {'devtools': devtools})

# 개발툴 상세
def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'devtools/devtool_detail.html', {'devtool': devtool})

# 개발툴 등록
def devtool_add(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtools:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'devtools/devtool_form.html', {'form': form})

# 개발툴 수정
def devtool_edit(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('devtools:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'devtools/devtool_form.html', {'form': form})

# 개발툴 삭제
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtools:devtool_list')
