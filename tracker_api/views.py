
# Create your views here.
import datetime
from gettext import translation
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Individuals, Admin, Vaccinationhistory, Vaccinationtypes
from .serializers import IndividualSerializer, AdminSerializer, VaccinationHistorySerializer, VaccinationTypesSerializer
from django.contrib.auth.hashers import make_password, check_password # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import json
from django.contrib.auth import authenticate # type: ignore
from django.shortcuts import render # type: ignore
from django.db import transaction # type: ignore
import random


# Admin Registration API
class AdminRegisterView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])  # Hash the password
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Login API
class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            admin = Admin.objects.get(username=username)
            if check_password(password, admin.password):
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            return JsonResponse({"message": "Login successful!"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Method not allowed"}, status=405)

# Individual CRUD APIs
class PublicIndividualView(APIView): 
    def get(self, request, patient_number, format=None):
        # Filter the individual by patient_number
        try:
            individual = Individuals.objects.get(patient_number=patient_number)
        except Individuals.DoesNotExist:
            raise NotFound(detail="Individual with this patient_number does not exist.") # type: ignore

        # Serialize the individual data, including nested vaccination history
        serializer = IndividualSerializer(individual)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class UpdateIndividualView(APIView):
    def put(self, request, patient_number, format=None):
        """
        Update individual details, vaccination history, and vaccination types using patient_number.
        """
        try:
            # Retrieve the individual by patient_number
            individual = Individuals.objects.get(patient_number=patient_number)
        except Individuals.DoesNotExist:
            return Response(
                {"error": "Individual with this patient_number does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Extract data for individual, vaccination history, and vaccination type
        individual_data = request.data.get('individual', {})
        vaccination_history_data = request.data.get('vaccination_history', [])

        try:
            with transaction.atomic():  # Ensure all updates are atomic
                # Update individual details
                individual_serializer = IndividualSerializer(individual, data=individual_data, partial=True)
                if individual_serializer.is_valid():
                    individual_serializer.save()
                else:
                    return Response(individual_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Update vaccination history and types
                for history in vaccination_history_data:
                    history_id = history.get('history_id')
                    if not history_id:
                        continue  # Skip if history_id is not provided

                    try:
                        vaccination_history = Vaccinationhistory.objects.get(history_id=history_id, individual=individual)
                    except Vaccinationhistory.DoesNotExist:
                        return Response(
                            {"error": f"Vaccination history with ID {history_id} does not exist for this individual."},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    # Update vaccination type if provided
                    vaccination_type_data = history.get('vaccination_type', {})
                    if vaccination_type_data:
                        vaccination_type = vaccination_history.vaccination_type
                        vaccination_type_serializer = VaccinationTypesSerializer(vaccination_type, data=vaccination_type_data, partial=True)
                        if vaccination_type_serializer.is_valid():
                            vaccination_type_serializer.save()
                        else:
                            return Response(vaccination_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # Update vaccination history
                    history_serializer = VaccinationHistorySerializer(vaccination_history, data=history, partial=True)
                    if history_serializer.is_valid():
                        history_serializer.save()
                    else:
                        return Response(history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    "message": "Individual details, vaccination history, and types updated successfully.",
                    "individual": individual_serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteIndividualView(APIView):
    def delete(self, request, patient_number):
        try:
            # Fetch the individual
            individual = Individuals.objects.get(patient_number=patient_number)

            with transaction.atomic():  # Ensure atomic deletion
                # Get all vaccination history entries for this individual
                vaccination_histories = Vaccinationhistory.objects.filter(individual=individual)

                # Delete all related vaccination types
                for history in vaccination_histories:
                    vaccination_type = history.vaccination_type
                    history.delete()  # Delete vaccination history
                    # Check if the vaccination type is associated with other histories
                    if not Vaccinationhistory.objects.filter(vaccination_type=vaccination_type).exists():
                        vaccination_type.delete()  # Delete vaccination type if no other references exist

                # Delete the individual
                individual.delete()

            return Response({"message": "Individual and related data deleted successfully."}, status=status.HTTP_200_OK)

        except Individuals.DoesNotExist:
            return Response({"error": "Individual not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminCreateIndividualsView(APIView):
    def post(self, request):
        individuals_data = request.data.get("individual")
        vaccination_data = request.data.get("vaccination")

        # Validate if individual data is provided
        if not individuals_data:
            return Response(
                {"error": "Individual data is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract individual data
        first_name = individuals_data.get("first_name")
        last_name = individuals_data.get("last_name")
        birth_date = individuals_data.get("birth_date")
        gender = individuals_data.get("gender")
        contact_info = individuals_data.get("contact_info")

        # Validate individual fields
        if not all([first_name, last_name, birth_date, gender, contact_info]):
            return Response(
                {"error": "All individual fields (first_name, last_name, birth_date, gender, contact_info) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():  # Ensure atomicity
                # Generate a unique random 6-digit individual_id
                while True:
                    random_individual_id = random.randint(100000, 999999)
                    # Ensure the random ID is unique
                    if not Individuals.objects.filter(patient_number=random_individual_id).exists():
                        break  # Exit the loop when a unique ID is found

                # Create the individual with the random individual_id
                individual = Individuals.objects.create(
                    patient_number=random_individual_id,  # Set the random 6-digit individual_id
                    first_name=first_name,
                    last_name=last_name,
                    birth_date=birth_date,
                    gender=gender,
                    contact_info=contact_info
                )

                # Handle vaccination data
                if vaccination_data:
                    vaccination_name = vaccination_data.get("vaccination_name", "Default Vaccine")
                    manufacturer = vaccination_data.get("manufacturer", "Default Manufacturer")
                    description = vaccination_data.get("description", "Automatically created vaccination type")
                    
                    # Create vaccination type if provided
                    vaccination_type = Vaccinationtypes.objects.create(
                        vaccination_name=vaccination_name,
                        manufacturer=manufacturer,
                        description=description
                    )
                else:
                    # Default vaccination type
                    vaccination_type = Vaccinationtypes.objects.create(
                        vaccination_name="Default Vaccine",
                        manufacturer="Default Manufacturer",
                        description="Automatically created vaccination type"
                    )

                # Create the vaccination history using the individual instance
                vaccination_history = Vaccinationhistory.objects.create(
                    individual=individual,  # Use the actual individual instance here
                    vaccination_type=vaccination_type,
                    vaccination_date=datetime.date.today(),
                    vaccination_status="Pending"  # Default status
                )

                # Ensure that patient_number is set correctly in Vaccinationhistory (it must reference the individual instance)
                vaccination_history.patient_number = individual  # Assign the whole individual instance here
                vaccination_history.save()  # Save the updated vaccination history with patient_number as a ForeignKey

                # Serialize the individual, vaccination type, and vaccination history
                individual_serializer = IndividualSerializer(individual)
                vaccination_type_serializer = VaccinationTypesSerializer(vaccination_type)
                vaccination_history_serializer = VaccinationHistorySerializer(vaccination_history)

                # Return a successful response with serialized data
                return Response({
                    "individual": individual_serializer.data,
                    "vaccination_type": vaccination_type_serializer.data,
                    "vaccination_history": vaccination_history_serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle unexpected errors and return detailed message
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminGetUsersView(APIView):
  def get(self, request):
        try:
            # Retrieve all individuals from the database
            individuals = Individuals.objects.all()

            # Serialize all individual data, including nested vaccination history and types
            individual_serializer = IndividualSerializer(individuals, many=True)

            # Return the response with nested vaccination history and types
            return Response({
                "individuals": individual_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def landing_page(request):
    return render(request, "vaccination tracker/index.html")

def admin_dashboard(request):
    return render(request, "vaccination tracker/admin-dashboard.html")

def login(request):
    return render(request, "vaccination tracker/admin-login.html")

def signup(request):
    return render(request, "vaccination tracker/admin-signup.html")