   # C:\sistema_igreja\membros\forms.py
from django import forms
from .models import Frequencia, Membro, Celula, Reuniao # <--- Adicione Celula aqui

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_adesao': forms.DateInput(attrs={'type': 'date'}),
        }

class CelulaForm(forms.ModelForm):
    class Meta:
        model = Celula
        fields = '__all__'

class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = '__all__'
        widgets = {
            'data_reuniao': forms.DateInput(attrs={'type': 'date'}),
            'hora_reuniao': forms.TimeInput(attrs={'type': 'time'}),
        }

class FrequenciaForm(forms.Form): # <--- Mude de forms.ModelForm para forms.Form
    def __init__(self, *args, **kwargs):
        self.reuniao = kwargs.pop('reuniao', None)
        membros = kwargs.pop('membros', [])
        super().__init__(*args, **kwargs)

        if not self.reuniao:
            raise ValueError("FrequenciaForm requires a 'reuniao' instance.")

        # Cria um campo de checkbox para cada membro
        for membro in membros:
            # Define o nome do campo como 'membro_<id_do_membro>'
            field_name = f'membro_{membro.pk}'
            # Verifica se já existe um registro de frequência para esta reunião e membro
            initial_presente = False
            if self.reuniao and membro:
                try:
                    frequencia_existente = Frequencia.objects.get(reuniao=self.reuniao, membro=membro)
                    initial_presente = frequencia_existente.presente
                except Frequencia.DoesNotExist:
                    pass # Nenhuma frequência existente, mantém o padrão False

            self.fields[field_name] = forms.BooleanField(
                label=f'{membro.nome_completo}',
                required=False, # Não é obrigatório marcar presença
                initial=initial_presente, # Define o estado inicial do checkbox
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )

    def save(self):
        # Salva os dados de frequência
        if not self.reuniao:
            raise ValueError("Cannot save FrequenciaForm without a 'reuniao' instance.")

        for field_name, presente in self.cleaned_data.items():
            if field_name.startswith('membro_'):
                membro_pk = field_name.split('_')[1]
                membro = Membro.objects.get(pk=membro_pk)

                # Atualiza ou cria o registro de frequência
                frequencia, created = Frequencia.objects.update_or_create(
                    reuniao=self.reuniao,
                    membro=membro,
                    defaults={'presente': presente}
                )
