from django.urls import path # type: ignore
from .views import AdminRegisterView, AdminLoginView, PublicIndividualView,UpdateIndividualView,AdminGetUsersView,DeleteIndividualView,AdminCreateIndividualsView
from tracker_api import views

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin_register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('individual/<int:patient_number>/', PublicIndividualView.as_view(), name='individual_detail'),
    path('admin/update/<int:patient_number>/', UpdateIndividualView.as_view(), name='update_individual'),
    path('admin/delete/<int:patient_number>/', DeleteIndividualView.as_view(), name='delete_individual'),
    path('individual_with_vaccination/', AdminCreateIndividualsView.as_view(), name='create_individual_with_vaccination'),
    path('retrieveindividuals/', AdminGetUsersView.as_view(), name='individuals_vaccination_data'),
    path('landing_page', views.landing_page, name='landing_page'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]

