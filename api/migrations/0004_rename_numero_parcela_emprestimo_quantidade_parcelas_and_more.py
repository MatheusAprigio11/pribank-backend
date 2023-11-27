# Generated by Django 4.2.7 on 2023-11-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_movimentacao_id_conta_destino'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emprestimo',
            old_name='numero_parcela',
            new_name='quantidade_parcelas',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='valor_parcela',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]