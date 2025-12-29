from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Importação necessária para o novo campo líder

# Modelo para a Célula
class Celula(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    # AJUSTADO: Agora o líder é vinculado diretamente a um usuário do sistema
    lider = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='celulas_lideradas')
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Célula"
        verbose_name_plural = "Células"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Modelo para o Membro
class Membro(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
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
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

# Modelo para a Reunião
class Reuniao(models.Model):
    celula = models.ForeignKey(Celula, on_delete=models.CASCADE, related_name='reunioes')
    data_reuniao = models.DateField(default=timezone.now)
    hora_reuniao = models.TimeField(default='00:00:00')
    tema = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"
        unique_together = ('celula', 'data_reuniao', 'hora_reuniao') 
        ordering = ['-data_reuniao', '-hora_reuniao'] 

    def __str__(self):
        return f"Reunião da Célula {self.celula.nome} em {self.data_reuniao.strftime('%d/%m/%Y')} às {self.hora_reuniao.strftime('%H:%M')}"

# Modelo para a Frequência
class Frequencia(models.Model):
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        unique_together = ('reuniao', 'membro')
        ordering = ['reuniao__data_reuniao', 'reuniao__hora_reuniao', 'membro__nome_completo']

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        return f"{self.membro.nome_completo} - {status} na Reunião de {self.reuniao.data_reuniao.strftime('%d/%m/%Y')} às {self.reuniao.hora_reuniao.strftime('%H:%M')}"