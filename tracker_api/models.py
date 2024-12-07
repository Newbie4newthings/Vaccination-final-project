from django.db import models # type: ignore


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'




class Individuals(models.Model):
    patient_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'individuals'


class Vaccinationhistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    individual = models.ForeignKey(Individuals, models.DO_NOTHING, blank=True, null=True)
    patient_number = models.ForeignKey(Individuals, models.DO_NOTHING, db_column='patient_number', to_field='patient_number', related_name='vaccinationhistory_patient_number_set', blank=True, null=True)
    vaccination_type = models.ForeignKey('Vaccinationtypes', models.DO_NOTHING, blank=True, null=True)
    vaccination_date = models.DateField(blank=True, null=True)
    vaccination_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vaccinationhistory'


class Vaccinationtypes(models.Model):
    vaccination_type_id = models.AutoField(primary_key=True)
    vaccination_name = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vaccinationtypes'