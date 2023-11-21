# Generated by Django 4.2.7 on 2023-11-21 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('id_cartao', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=16)),
                ('validade', models.DateField()),
                ('cvv', models.IntegerField()),
                ('bandeira', models.CharField(max_length=15)),
                ('situacao', models.BooleanField(default=True, verbose_name='Ativo?')),
            ],
            options={
                'verbose_name': 'Cartao',
                'verbose_name_plural': 'Cartoes',
                'ordering': ['id_cartao'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('foto', models.CharField(max_length=255)),
                ('dataNascimento', models.DateField()),
                ('usuario', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=30)),
                ('telefone', models.CharField(max_length=11)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id_cliente'],
            },
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('id_conta', models.AutoField(primary_key=True, serialize=False)),
                ('agencia', models.IntegerField(verbose_name='Agencia')),
                ('conta', models.CharField(max_length=10)),
                ('limite', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ativa', models.BooleanField(default=True, verbose_name='Ativa?')),
            ],
            options={
                'verbose_name': 'Conta',
                'verbose_name_plural': 'Contas',
                'ordering': ['id_conta'],
            },
        ),
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('id_movimentacao', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dataMovimentacao', models.DateField(auto_now=True)),
                ('tipo', models.CharField(max_length=15)),
                ('id_cartao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes_cartao', to='api.cartao')),
                ('id_conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes_conta', to='api.conta')),
            ],
            options={
                'verbose_name': 'Movimentacao',
                'verbose_name_plural': 'Movimentacoes',
                'ordering': ['id_movimentacao'],
            },
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('id_emprestimo', models.AutoField(primary_key=True, serialize=False)),
                ('data_solicitacao', models.DateField(auto_now_add=True)),
                ('valor_solicitado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('juros', models.DecimalField(decimal_places=2, max_digits=10)),
                ('numero_parcela', models.IntegerField()),
                ('aprovado', models.BooleanField()),
                ('data_aprovacao', models.DateField(auto_now_add=True)),
                ('observacao', models.TextField(blank=True, default='')),
                ('id_conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprestimo_conta', to='api.conta')),
            ],
            options={
                'verbose_name': 'Emprestimo',
                'verbose_name_plural': 'Emprestimos',
                'ordering': ['id_emprestimo'],
            },
        ),
    ]
