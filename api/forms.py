from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ClienteConta

class ClienteCreateForm(UserCreationForm):
    
    class Meta:
        model = ClienteConta
        fields = ['foto', 'first_name', 'last_name', 'cpf', 'dataNascimento', 'telefone', 'token']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user = self.cleaned_data['username']  # Corrigido aqui
        
        if commit:
            user.save()
        
        return user

    

class ClienteChangeForm(UserChangeForm):
    
    class Meta:
        model = ClienteConta
        fields = ['foto', 'first_name', 'last_name', 'cpf', 'dataNascimento', 'telefone', 'token']