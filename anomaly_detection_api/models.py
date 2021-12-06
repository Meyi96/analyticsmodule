# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Comitee(models.Model):
    comitee_id = models.AutoField(primary_key=True)
    comitee_name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'comitee'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    abreviation = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'country'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    date_reported = models.DateField()
    status = models.CharField(max_length=15)
    report_report = models.ForeignKey('Report', models.DO_NOTHING)
    country_country = models.ForeignKey(Country, models.DO_NOTHING)
    age = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    date_notified = models.DateField()
    gender = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'event'


class Experiment(models.Model):
    experiment_id = models.AutoField(primary_key=True)
    experiment_description = models.CharField(max_length=256, blank=True, null=True)
    comitee_comitee = models.ForeignKey(Comitee, models.DO_NOTHING)
    is_active = models.BooleanField()
    protocol = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'experiment'


class ExperimentMoleculeComposition(models.Model):
    exp_mol_comp_id = models.AutoField(primary_key=True)
    molecule_molecule = models.ForeignKey('Molecule', models.DO_NOTHING)
    experiment_experiment = models.ForeignKey(Experiment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'experiment_molecule_composition'


class ExperimentSymptomRegister(models.Model):
    exp_symptom_reg_id = models.AutoField(primary_key=True)
    counter = models.IntegerField()
    experiment_experiment = models.ForeignKey(Experiment, models.DO_NOTHING)
    symptom_symptom = models.ForeignKey('Symptom', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'experiment_symptom_register'


class Laboratory(models.Model):
    laboratory_id = models.AutoField(primary_key=True)
    laboratory_name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'laboratory'


class Molecule(models.Model):
    molecule_id = models.AutoField(primary_key=True)
    molecule_name = models.CharField(max_length=30)
    laboratory_laboratory = models.ForeignKey(Laboratory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'molecule'


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_name = models.CharField(max_length=30)
    person_email = models.CharField(max_length=50)
    rolee_rolee = models.ForeignKey('Rolee', models.DO_NOTHING)
    pd = models.CharField(max_length=300)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    date_recieved = models.DateField()
    date_registered = models.DateField()
    effect_patient = models.CharField(max_length=256, blank=True, null=True)
    effect_medicine = models.CharField(max_length=256, blank=True, null=True)
    person_person = models.ForeignKey(Person, models.DO_NOTHING)
    time_period_time_period = models.ForeignKey('TimePeriod', models.DO_NOTHING)
    still_open = models.BooleanField()
    experiment_experiment = models.ForeignKey(Experiment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'report'


class Rolee(models.Model):
    rolee_id = models.AutoField(primary_key=True)
    rolee_name = models.CharField(max_length=30)
    rolee_description = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'rolee'


class Susars(models.Model):
    susars_id = models.AutoField(primary_key=True)
    assesment_level = models.IntegerField()
    symptom_symptom = models.ForeignKey('Symptom', models.DO_NOTHING)
    molecule_molecule = models.ForeignKey(Molecule, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'susars'


class Symptom(models.Model):
    symptom_id = models.AutoField(primary_key=True)
    symptom_title = models.CharField(max_length=380)
    symptom_code = models.CharField(max_length=10, blank=True, null=True)
    assesment_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symptom'


class SymptomEventRegister(models.Model):
    symp_event_id = models.AutoField(primary_key=True)
    symptom_symptom = models.ForeignKey(Symptom, models.DO_NOTHING)
    event_event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'symptom_event_register'


class TimePeriod(models.Model):
    time_period_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'time_period'