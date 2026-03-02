import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Workflow, Node, Edge

@login_required
def workflow_list(request):
    workflows = Workflow.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'workflows/list.html', {'workflows': workflows})

@login_required
def workflow_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description', '')
        if title:
            wf = Workflow.objects.create(user=request.user, title=title, description=desc)
            return redirect('workflows:canvas', pk=wf.pk)
    return render(request, 'workflows/create.html')

@login_required
def workflow_canvas(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk, user=request.user)
    return render(request, 'workflows/canvas.html', {'workflow': workflow})

# API Endpoints for the Interactive Canvas
@login_required
def api_load_workflow(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk, user=request.user)
    
    nodes = []
    for n in workflow.nodes.all():
        nodes.append({
            'id': n.id,
            'type': n.type,
            'label': n.label,
            'pos_x': n.pos_x,
            'pos_y': n.pos_y
        })
        
    edges = []
    for e in workflow.edges.all():
        edges.append({
            'id': e.id,
            'source': e.source.id,
            'target': e.target.id
        })
        
    return JsonResponse({'nodes': nodes, 'edges': edges})

@csrf_exempt
@login_required
def api_save_workflow(request, pk):
    if request.method == 'POST':
        workflow = get_object_or_404(Workflow, pk=pk, user=request.user)
        try:
            data = json.loads(request.body)
            nodes_data = data.get('nodes', [])
            edges_data = data.get('edges', [])
            
            # Clear existing (simple approach for MVP: destroy and recreate)
            workflow.nodes.all().delete()
            
            node_mapping = {} # frontend_id -> db_id
            
            for n_data in nodes_data:
                node = Node.objects.create(
                    workflow=workflow,
                    type=n_data['type'],
                    label=n_data['label'],
                    pos_x=n_data['pos_x'],
                    pos_y=n_data['pos_y']
                )
                node_mapping[n_data['id']] = node
                
            for e_data in edges_data:
                source_node = node_mapping.get(e_data['source'])
                target_node = node_mapping.get(e_data['target'])
                if source_node and target_node:
                    Edge.objects.create(
                        workflow=workflow,
                        source=source_node,
                        target=target_node
                    )
            
            # Update workflow timestamp
            workflow.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)
