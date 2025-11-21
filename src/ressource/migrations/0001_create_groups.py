from django.db import migrations

def create_initial_groups(apps, schema_editor):
    # Récupère le modèle Group via l'API historique de migration
    Group = apps.get_model('auth', 'Group')
    
    # Liste des noms de groupes à créer
    group_names = [
        "Superadmin",
        "Administrateur",
        "Gestionnaire",
        "Utilisateur",
    ]
    
    # Crée chaque groupe s'il n'existe pas déjà
    for name in group_names:
        Group.objects.get_or_create(name=name)

def delete_initial_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    group_names = [
        "Superadmin",
        "Administrateur",
        "Gestionnaire",
        "Utilisateur",
    ]
    Group.objects.filter(name__in=group_names).delete()

class Migration(migrations.Migration):

    initial = True

    # Dépendance minimale sur l'application "auth"
    dependencies = [
        ('auth',"0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_groups, delete_initial_groups),
    ]
