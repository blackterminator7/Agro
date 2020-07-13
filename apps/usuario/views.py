import json
from django.shortcuts import render#, redirect
from django.urls import reverse_lazy
#from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect#,HttpResponse,JsonResponse
#from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from apps.usuario.models import Usuario
from apps.usuario.forms import FormularioLogin, FormularioUsuario
#from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosRequeridosUsuariosMixin

# Vista para el menu de inicio
def index(request):
    return render(
        request,
        'base/base.html',
    )


class Login(FormView):
    template_name = 'usuario/login1.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('usuario:index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def logoutUsuario(request):
   	logout(request)
   	return HttpResponseRedirect(reverse_lazy('usuario:login'))	



class ListadoUsuario(ListView):
    model=Usuario
    template_name='usuario/listar_usuario.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)

class RegistrarUsuario(CreateView):
    model=Usuario
    form_class=FormularioUsuario
    template_name='usuario/crear_usuario.html'

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario=Usuario(
                email=form.cleaned_data.get('email'),
                username=form.cleaned_data.get('username'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('usuario:listar_usuarios')
        else:
            return render(request, self.template_name,{'form':form})