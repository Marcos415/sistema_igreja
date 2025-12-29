# C:\sistema_igreja\membros\forms.py
from django import forms
from .models import Frequencia, Membro, Celula, Reuniao

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_adesao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CelulaForm(forms.ModelForm):
    class Meta:
        model = Celula
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'lider': forms.Select(attrs={'class': 'form-control'}),
        }

class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = '__all__'
        widgets = {
            'data_reuniao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_reuniao': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'celula': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FrequenciaForm(forms.Form):
    """
    Formulário dinâmico para registrar presença. 
    Gera um checkbox para cada membro da célula vinculada à reunião.
    """
    def __init__(self, *args, **kwargs):
        self.reuniao = kwargs.pop('reuniao', None)
        membros = kwargs.pop('membros', [])
        super().__init__(*args, **kwargs)

        if not self.reuniao:
            raise ValueError("FrequenciaForm requer uma instância de 'reuniao'.")

        # Cria um campo de checkbox para cada membro na lista fornecida
        for membro in membros:
            field_name = f'membro_{membro.pk}'
            
            # Busca se já existe um registro salvo para evitar perda de dados ao reabrir
            initial_presente = False
            if self.reuniao:
                frequencia_existente = Frequencia.objects.filter(
                    reuniao=self.reuniao, 
                    membro=membro
                ).first()
                if frequencia_existente:
                    initial_presente = frequencia_existente.presente

            self.fields[field_name] = forms.BooleanField(
                label=f'{membro.nome_completo}',
                required=False,
                initial=initial_presente,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )

    def save(self):
        """
        Salva ou atualiza os registros de frequência no banco de dados.
        """
        if not self.reuniao:
            raise ValueError("Não é possível salvar sem uma instância de 'reuniao'.")

        for field_name, presente in self.cleaned_data.items():
            if field_name.startswith('membro_'):
                membro_pk = field_name.split('_')[1]
                # O update_or_create evita duplicatas se o líder salvar o formulário duas vezes
                Frequencia.objects.update_or_create(
                    reuniao=self.reuniao,
                    membro_id=membro_pk,
                    defaults={'presente': presente}
                )