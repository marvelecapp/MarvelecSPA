from django.db import migrations

# Ajustes pedidos por la empresa tras usar la app en obra ("Arreglos a la app").
# Se renombran los tipos en vez de crear otros: así las incidencias ya registradas los conservan.
RENOMBRES = [
    ('Sin canalización', 'Error canalización (lugar o posición errado)'),
    ('No conecta', 'No conecta (cable perdido)'),
]
NUEVOS = [('Otros', False, 99)]


def aplicar(apps, schema_editor):
    TipoIncidencia = apps.get_model('marvelec_app', 'TipoIncidencia')
    for viejo, nuevo in RENOMBRES:
        if not TipoIncidencia.objects.filter(nombre=nuevo).exists():
            TipoIncidencia.objects.filter(nombre=viejo).update(nombre=nuevo)
    for nombre, falla, orden in NUEVOS:
        TipoIncidencia.objects.get_or_create(
            nombre=nombre, defaults={'es_falla_certificacion': falla, 'orden': orden}
        )


def revertir(apps, schema_editor):
    TipoIncidencia = apps.get_model('marvelec_app', 'TipoIncidencia')
    for viejo, nuevo in RENOMBRES:
        if not TipoIncidencia.objects.filter(nombre=viejo).exists():
            TipoIncidencia.objects.filter(nombre=nuevo).update(nombre=viejo)


class Migration(migrations.Migration):

    dependencies = [
        ('marvelec_app', '0012_alter_avancepunto_etapa'),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
