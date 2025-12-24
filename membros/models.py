# membros/models.py
from django.db import models
from django.utils import timezone

# Modelo para a Célula
class Celula(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    lider = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Célula"
        verbose_name_plural = "Células"
        ordering = ['nome'] # Ordena células por nome

    def __str__(self):
        return self.nome

# Modelo para o Membro
class Membro(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'), # Opcional: para outras identidades
    ]

    nome_completo = models.CharField(max_length=200, unique=True)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    celula = models.ForeignKey(Celula, on_delete=models.SET_NULL, null=True, blank=True, related_name='membros')
    data_adesao = models.DateField(default=timezone.now)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"
        ordering = ['nome_completo'] # Ordena membros por nome

    def __str__(self):
        return self.nome_completo

# Modelo para a Reunião
class Reuniao(models.Model):
    celula = models.ForeignKey(Celula, on_delete=models.CASCADE, related_name='reunioes')
    data_reuniao = models.DateField(default=timezone.now)
    # >>> CAMPO ADICIONADO/CORRIGIDO <<<
    hora_reuniao = models.TimeField(default='00:00:00') # Valor padrão para evitar erro ao aplicar migração
    tema = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"
        # Ajustado para incluir hora_reuniao na unicidade, pois agora é parte da identificação
        unique_together = ('celula', 'data_reuniao', 'hora_reuniao') 
        # Ajustado para ordenar também pela hora da reunião
        ordering = ['-data_reuniao', '-hora_reuniao'] 

    def __str__(self):
        # Ajuste para incluir a hora na representação do objeto
        return f"Reunião da Célula {self.celula.nome} em {self.data_reuniao.strftime('%d/%m/%Y')} às {self.hora_reuniao.strftime('%H:%M')}"

# Modelo para a Frequência (presença de membro em reunião)
class Frequencia(models.Model):
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(default=timezone.now) # Adicionado para registrar quando a frequência foi lançada
    
    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        unique_together = ('reuniao', 'membro') # Garante que um membro só tem uma frequência por reunião
        # Ajustado para ordenar também pela hora da reunião
        ordering = ['reuniao__data_reuniao', 'reuniao__hora_reuniao', 'membro__nome_completo']

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        # Ajuste para mostrar a hora da reunião no __str__
        return f"{self.membro.nome_completo} - {status} na Reunião de {self.reuniao.data_reuniao.strftime('%d/%m/%Y')} às {self.reuniao.hora_reuniao.strftime('%H:%M')}"