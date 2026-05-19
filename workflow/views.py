from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import JobApplication, StageLog, STAGES
from .engine import WorkflowRegistry


STAGE_ORDER = ['applied', 'screening', 'interview', 'offer', 'accepted']


def workflow_home(request):
    apps = JobApplication.objects.all()
    stage_filter = request.GET.get('stage', '')
    if stage_filter:
        apps = apps.filter(stage=stage_filter)

    stats = {s: JobApplication.objects.filter(stage=s).count() for s, _ in STAGES}
    return render(request, 'workflow/home.html', {
        'applications': apps,
        'stages': STAGES,
        'stats': stats,
        'active_filter': stage_filter,
        'workflows': WorkflowRegistry.all(),
    })


def add_application(request):
    if request.method == 'POST':
        app = JobApplication.objects.create(
            company=request.POST['company'],
            role=request.POST['role'],
            location=request.POST.get('location', ''),
            url=request.POST.get('url', ''),
            notes=request.POST.get('notes', ''),
        )
        StageLog.objects.create(application=app, from_stage='', to_stage='applied', note='Application created')
        return redirect('workflow_home')
    return render(request, 'workflow/add.html')


def detail(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'workflow/detail.html', {'app': app, 'stages': STAGES, 'stage_order': STAGE_ORDER})


def advance_stage(request, pk):
    if request.method == 'POST':
        app = get_object_or_404(JobApplication, pk=pk)
        new_stage = request.POST.get('stage')
        note = request.POST.get('note', '')
        if new_stage in dict(STAGES):
            StageLog.objects.create(application=app, from_stage=app.stage, to_stage=new_stage, note=note)
            app.stage = new_stage
            app.save()
    return redirect('detail', pk=pk)


def delete_application(request, pk):
    get_object_or_404(JobApplication, pk=pk).delete()
    return redirect('workflow_home')


def run_workflow(request, name):
    if request.method == 'POST':
        workflow = WorkflowRegistry.get(name)
        if not workflow:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        log = workflow.run({'input': request.POST.get('input', 'sample data')})
        return JsonResponse({'workflow': name, 'log': log})
    return JsonResponse({'error': 'POST required'}, status=405)
