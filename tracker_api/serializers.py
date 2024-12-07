from rest_framework import serializers # type: ignore
from .models import Admin, Individuals, Vaccinationhistory, Vaccinationtypes

# Serializer for Admin model
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['admin_id', 'username', 'password', 'first_name', 'last_name', 'contact_info', 'role']

# Serializer for Individuals model
class IndividualSerializer(serializers.ModelSerializer):
    # Include nested VaccinationHistorySerializer to get vaccination data
    vaccination_history = serializers.SerializerMethodField()

    class Meta:
        model = Individuals
        fields = ['patient_number', 'first_name', 'last_name', 'birth_date', 'gender', 'contact_info', 'vaccination_history']

    def get_vaccination_history(self, obj):
        # Get all vaccination history entries for this individual
        vaccination_history = Vaccinationhistory.objects.filter(individual=obj)
        # Serialize each vaccination history entry
        return VaccinationHistorySerializer(vaccination_history, many=True).data

# Serializer for VaccinationTypes model
class VaccinationTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccinationtypes
        fields = ['vaccination_type_id', 'vaccination_name', 'manufacturer', 'description']


# Serializer for VaccinationHistory model
class VaccinationHistorySerializer(serializers.ModelSerializer):
    # Nested vaccination_type serializer to include the vaccination type details
    vaccination_type = VaccinationTypesSerializer(read_only=True)

    class Meta:
        model = Vaccinationhistory
        fields = ['history_id', 'vaccination_date', 'vaccination_status', 'vaccination_type']


