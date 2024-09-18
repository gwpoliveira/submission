from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, SubmissionForm, ProfileForm, ComponentFormSet
from .models import Submission, Profile, ThematicAxis, Modality
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa  # Biblioteca para converter HTML em PDF
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect

# Função para verificar se o usuário é administrador
def is_admin(user):
    return user.is_superuser

# Página inicial
def home(request):
    return render(request, 'home.html')

# Registro de usuários
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # O perfil será criado automaticamente pelo signal
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)

                if user is not None:
                    login(request, user)
                    messages.success(request, 'Registro realizado com sucesso! Bem-vindo(a) ao sistema.')
                    return redirect('home')
                else:
                    form.add_error(None, 'Erro ao autenticar o usuário. Por favor, tente novamente.')
            except IntegrityError:
                messages.success(request, 'Registro realizado com sucesso! Bem-vindo(a) ao sistema.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login de usuários
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout de usuários
def logout_user(request):
    logout(request)
    return redirect('home')

# Página de sucesso de submissão
def submission_success(request):
    return render(request, 'submission_success.html')

# Formulário de submissão de trabalhos
@login_required
def submission_form(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        submission_form = SubmissionForm(request.POST, request.FILES)
        component_formset = ComponentFormSet(request.POST, request.FILES)

        if profile_form.is_valid() and submission_form.is_valid() and component_formset.is_valid():
            # Primeiro, salva o perfil do usuário
            profile_form.save()

            # Salva a submissão sem comitar (commit=False) para ter acesso ao objeto de submissão
            submission = submission_form.save(commit=False)
            submission.user = request.user.profile  # Atribui o usuário à submissão
            submission.save()  # Agora salva a submissão no banco de dados

            # Associa a submissão aos componentes e salva o formset
            components = component_formset.save(commit=False)
            for component in components:
                component.submission = submission  # Define a submissão para cada componente
                component.save()

            # Agora salva o formset completo
            component_formset.save()

            return redirect('submission_success')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        submission_form = SubmissionForm()
        component_formset = ComponentFormSet()

    return render(request, 'submission_form.html', {
        'profile_form': profile_form,
        'submission_form': submission_form,
        'component_formset': component_formset
    })

# Painel administrativo com filtro e paginação
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    modalidade = request.GET.get('modality')
    eixo_tematico = request.GET.get('thematic_axis')
    usuario = request.GET.get('username')
    status = request.GET.get('status')

    # Carregar todas as submissões
    submissions = Submission.objects.all().order_by('-data_envio')

    # Aplicar filtros
    if modalidade:
        submissions = submissions.filter(modality__id=modalidade)
    if eixo_tematico:
        submissions = submissions.filter(thematic_axis__id=eixo_tematico)
    if usuario:
        submissions = submissions.filter(user__user__username__icontains=usuario)
    if status:
        submissions = submissions.filter(status=status)

    # Carregar dados adicionais para os filtros
    thematic_axes = ThematicAxis.objects.all()
    modalities = Modality.objects.all()

    # Paginação
    paginator = Paginator(submissions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {
        'submissions': page_obj,
        'thematic_axes': thematic_axes,
        'modalities': modalities
    })

# Detalhe da submissão do usuário com possibilidade de atualização do status
@login_required
@user_passes_test(is_admin)
def user_submission_detail(request, submission_id):
    submission = Submission.objects.get(id=submission_id)

    if request.method == 'POST':
        submission.status = request.POST.get('status')
        submission.observacao = request.POST.get('observacao', '')
        submission.save()
        messages.success(request, 'Submissão atualizada com sucesso.')
        return redirect('admin_dashboard')

    return render(request, 'user_submission_detail.html', {
        'submission': submission,
        'arquivo': submission.arquivo.url if submission.arquivo else None,
        'comprovante': submission.user.comprovante_pagamento.url if submission.user.comprovante_pagamento else None
    })

# Função para atualizar o status da submissão e adicionar observações
@login_required
@user_passes_test(is_admin)
def update_submission_status(request, submission_id):
    submission = Submission.objects.get(id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        observacao = request.POST.get('observacao')
        submission.status = status
        submission.observacao = observacao
        submission.save()

    return redirect('admin_dashboard')

# Página para visualizar submissões do usuário logado
@login_required
def view_submissions(request):
    submissions = Submission.objects.filter(user=request.user.profile)
    return render(request, 'submissions.html', {'submissions': submissions})

# Funções de sinal para criação e salvamento de perfil
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Outras páginas
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def generate_acceptance_letter(request, submission_id):
    submission = Submission.objects.get(id=submission_id)

    # Verifica se o usuário é superusuário ou autor da submissão
    if not (request.user.is_superuser or request.user.profile == submission.user):
        messages.error(request, 'Você não tem permissão para acessar esta carta de aceite.')
        return HttpResponseRedirect(reverse('home'))

    # Verifica se a submissão foi deferida
    if submission.status != 'DEFERIDO':
        messages.error(request, 'A carta de aceite só pode ser gerada para submissões deferidas.')
        return HttpResponseRedirect(reverse('user_submission_detail', args=[submission_id]))

    components = submission.components.all()

    # Renderiza o template da carta de aceite
    html = render_to_string('acceptance_letter.html', {
        'submission': submission,
        'components': components
    })

    # Gerar o PDF a partir do HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="carta_aceite_{submission_id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)

    # Marcar que a carta foi gerada
    submission.acceptance_letter_generated = True
    submission.save()

    return response
