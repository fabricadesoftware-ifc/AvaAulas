import datetime
from django.db import models

from django.utils import timezone


class NivelCurso(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.desc_nivel


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField
    nivel = models.ForeignKey(
        "NivelCurso", on_delete=models.RESTRICT, related_name="cursos"
    )

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField
    ano_letivo = models.IntegerField
    semestral = models.BooleanField()

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if (self.semestral) and (self.semestre == None):
            self.semestre = 1
        super(Disciplina, self).save(*args, **kwargs)


class Area(models.Model):
    nome = models.CharField(max_length=80)


class Professor(models.Model):
    nome = models.CharField(max_length=150)
    area = models.ForeignKey(
        "Area", on_delete=models.RESTRICT, related_name="professores"
    )

    def __str__(self):
        return self.nome


class Oferta(models.Model):
    class SemestreLetivo(models.IntegerChoices):
        PRIMEIRO = 1, "1º Semestre"
        SEGUNDO = 2, "2º Semestre"

    ano = models.IntegerField
    professor = models.ForeignKey(
        "Professor", on_delete=models.RESTRICT, related_name="disciplinas"
    )
    disciplina = models.ForeignKey(
        "Disciplina", on_delete=models.RESTRICT, related_name="professores"
    )
    semestre = models.IntegerField(
        choices=SemestreLetivo.choices,
        default=SemestreLetivo.PRIMEIRO,
        blank=True,
        null=True,
    )
    turma = models.CharField

    def __str__(self) -> str:
        return self.professor


class Formulario(models.Model):
    disciplina = models.ForeignKey("Disciplina", on_delete=models.RESTRICT)
    data_aula = models.DateField
    tema_aula = models.CharField(max_length=100)
    descricao_aula = models.CharField(max_length=500)
    data_limite_resposta = models.DateField

    def __str__(self):
        return self.tema_aula


class Pergunta(models.Model):
    TIPO_CHOICES = ("O", "Objetiva")("D", "Discursiva")
    pergunta_texto = models.CharField(max_length=200)
    formulario = models.ForeignKey("Formulario", on_delete=models.RESTRICT)
    tipo_pergunta = models.CharField(choices=TIPO_CHOICES, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.pergunta_texto


class Opcao(models.Model):
    class Meta:
        verbose_name_plural = "Opções"

    pergunta = models.ForeignKey(Pergunta, on_delete=models.RESTRICT)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto


class Resposta(models.Model):
    pergunta = models.ForeignKey("Pergunta", on_delete=models.RESTRICT)
    resposta = models.ForeignKey("Opcao", on_delete=models.RESTRICT)
    data_hora = models.DateTimeField

    def __str__(self):
        return self.resposta
