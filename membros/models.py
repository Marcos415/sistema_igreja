from django.db import models
from django.urls import reverse

class Celula(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    lider = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Célula"
        verbose_name_plural = "Células"
        ordering = ['nome'] # Ordena as células pelo nome

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('membros:listar_celulas') # Redireciona para a lista de células após adicionar/editar


class Membro(models.Model):
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # AQUI: Alterado o verbose_name para 'Data de Início'
    data_adesao = models.DateField(verbose_name='Data de Início')
    celula = models.ForeignKey(Celula, on_delete=models.SET_NULL, null=True, blank=True, related_name='membros')
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"
        ordering = ['nome_completo'] # Ordena os membros pelo nome completo

    def __str__(self):
        return self.nome_completo

    def get_absolute_url(self):
        return reverse('membros:listar_membros') # Redireciona para a lista de membros após adicionar/editar


class Reuniao(models.Model):
    tema = models.CharField(max_length=200)
    data_reuniao = models.DateField()
    hora_reuniao = models.TimeField()
    celula = models.ForeignKey(Celula, on_delete=models.CASCADE, related_name='reunioes')
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"
        ordering = ['-data_reuniao', '-hora_reuniao'] # Ordena as reuniões da mais recente para a mais antiga

    def __str__(self):
        return f"{self.tema} ({self.data_reuniao.strftime('%d/%m/%Y')} - {self.celula.nome})"

    def get_absolute_url(self):
        return reverse('membros:listar_reunioes') # Redireciona para a lista de reuniões após adicionar/editar


class Frequencia(models.Model):
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='frequencia')
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='frequencia')
    presente = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        # Garante que um membro só pode ter uma frequência por reunião
        unique_together = ('reuniao', 'membro')
        ordering = ['reuniao__data_reuniao', 'membro__nome_completo'] # Ordena por data da reunião e nome do membro

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        return f"{self.membro.nome_completo} - {self.reuniao.tema} ({self.reuniao.data_reuniao.strftime('%d/%m/%Y')}): {status}"
