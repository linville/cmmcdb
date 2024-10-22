# Generated by Django 2.2.7 on 2019-11-15 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(max_length=256, unique=True)),
                ('process', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('short', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaturityLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('practice_name', models.CharField(max_length=64, unique=True)),
                ('process_name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=1024)),
                ('capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practices', to='cmmcdb.Capability')),
                ('maturity_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmmcdb.MaturityLevel')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticeReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=64)),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmmcdb.Practice')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmmcdb.Reference')),
            ],
        ),
        migrations.AddField(
            model_name='capability',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capabilities', to='cmmcdb.Domain'),
        ),
    ]
