# Generated by Django 3.2.9 on 2021-12-01 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Eleicao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='Lula', max_length=666)),
                ('foto', models.ImageField(null=True, upload_to='')),
                ('votos', models.IntegerField(default=0)),
                ('numero', models.SmallIntegerField()),
                ('eleicao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Eleicao.eleicao')),
            ],
        ),
    ]