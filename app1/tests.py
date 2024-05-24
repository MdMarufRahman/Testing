from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import report, addRestaurentModel, contactUs as contactUsModel, team
from datetime import date, datetime
from django.contrib.auth import authenticate



# Create your tests here.

#User Homepage test
class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')  # Ensure 'home' matches the name in your urls.py

    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_content(self):
        response = self.client.get(self.url)
        # Check for a specific part of your HTML content that should be present
        self.assertContains(response, '<h1>Welcome, User!</h1>')



#Signup Unit testing
class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')  # Ensure 'signup' matches the name in your urls.py

    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('clickPicture'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_view_post_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password124'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your password and confirm password doesn't match")
        self.assertFalse(User.objects.filter(username='testuser').exists())



#Admin dashboard Unit testing
class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboardView')  # Ensure 'dashboard' matches the name in your urls.py

        # Create some test data
        User.objects.create(username='testuser1', email='test1@example.com', password='password123')
        User.objects.create(username='testuser2', email='test2@example.com', password='password123')

        report.objects.create(location="Location 1", latitude=10.0, longitude=20.0)
        report.objects.create(location="Location 2", latitude=15.0, longitude=25.0)

        addRestaurentModel.objects.create(commpanyName="Restaurant 1", expiryDate=date(2024, 12, 31))
        addRestaurentModel.objects.create(commpanyName="Restaurant 2", expiryDate=date(2025, 1, 31))

        contactUsModel.objects.create(contactMessage="Message 1", contactPhoneNumber="1234567890")
        contactUsModel.objects.create(contactMessage="Message 2", contactPhoneNumber="0987654321")

        team.objects.create(name="Team Member 1")
        team.objects.create(name="Team Member 2")

    def test_dashboard_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'adminDashboard.html')

    def test_dashboard_view_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['report_count'], 2)
        self.assertEqual(response.context['user_count'], 2)
        self.assertEqual(response.context['certificates_count'], 2)
        self.assertEqual(response.context['notification_count'], 2)
        self.assertEqual(len(response.context['reports']), 2)
        self.assertEqual(len(response.context['restaurents']), 2)
        self.assertEqual(len(response.context['availableTeam']), 2)



#Login Authentication Unit testing
class LoginViewTests(TestCase):

    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='testuser', password='testpass')

    def test_admin_login_success(self):
        client = Client()
        response = client.post(reverse('login'), {
            'logName': 'admin',
            'logPass': 'adminpass'
        })
        self.assertRedirects(response, reverse('dashboardView'))

    def test_normal_user_login_success(self):
        client = Client()
        response = client.post(reverse('login'), {
            'logName': 'testuser',
            'logPass': 'testpass'
        })
        self.assertRedirects(response, reverse('faceRecog'))

    def test_admin_login_failure(self):
        client = Client()
        response = client.post(reverse('login'), {
            'logName': 'admin',
            'logPass': 'wrongpass'
        })
        self.assertContains(response, "Username or Password is incorrect")

    def test_normal_user_login_failure(self):
        client = Client()
        response = client.post(reverse('login'), {
            'logName': 'testuser',
            'logPass': 'wrongpass'
        })
        self.assertContains(response, "Username or Password is incorrect")

    def test_get_request(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertTemplateUsed(response, 'index.html')
        


#Adding certificate from admin
class AddRestaurentViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_restaurent_view_get(self):
        response = self.client.get(reverse('addRestaurent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addRestaurent.html')

    def test_add_restaurent_view_post_success(self):
        data = {
            'company': 'Test Company',
            'issuedBy': 'Test Issuer',
            'expiryDate': '2024-12-31',
            'details': 'Test details for certification.'
        }
        response = self.client.post(reverse('addRestaurent'), data)
        self.assertRedirects(response, reverse('dashboardView'))

        # Verify that the data was saved in the database
        certification = addRestaurentModel.objects.get(commpanyName='Test Company')
        self.assertEqual(certification.issuedBy, 'Test Issuer')
        self.assertEqual(certification.expiryDate, datetime.strptime('2024-12-31', '%Y-%m-%d').date())
        self.assertEqual(certification.message, 'Test details for certification.')

    def test_add_restaurent_view_post_invalid(self):
        # Missing the 'company' field
        data = {
            'issuedBy': 'Test Issuer',
            'expiryDate': '2024-12-31',
            'details': 'Test details for certification.'
        }
        response = self.client.post(reverse('addRestaurent'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addRestaurent.html')
        self.assertContains(response, "All fields are required", html=True)

        # Verify that no entry was created in the database
        self.assertFalse(addRestaurentModel.objects.filter(issuedBy='Test Issuer').exists())



#Contact Us
class ContactUsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contactUs')  # Ensure this matches your URL pattern name
        self.data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }

    def test_contact_us_post_request(self):
        response = self.client.post(self.url, self.data)
        
        # Check if the entry is saved in the database
        self.assertEqual(contactUsModel.objects.count(), 1)
        contact_entry = contactUsModel.objects.first()
        self.assertEqual(contact_entry.contactFullName, self.data['full_name'])
        self.assertEqual(contact_entry.contactEmail, self.data['email'])
        self.assertEqual(contact_entry.contactPhoneNumber, int(self.data['phone_number']))
        self.assertEqual(contact_entry.contactSubject, self.data['subject'])
        self.assertEqual(contact_entry.contactMessage, self.data['message'])

        # Check if the response is a redirection to the homepage
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_contact_us_get_request(self):
        response = self.client.get(self.url)
        
        # Check if the GET request renders the contact page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')


#Available Team
class AddTeamViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('addTeam')  
        self.team_name = 'Test Team'

    def test_add_team_post_request(self):
        response = self.client.post(self.url, {'name': self.team_name})
        
        # Check if the entry is saved in the database
        self.assertEqual(team.objects.count(), 1)
        new_team = team.objects.first()
        self.assertEqual(new_team.name, self.team_name)

        # Check if the response is a redirection to the same addTeam page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

    def test_add_team_get_request(self):
        response = self.client.get(self.url)
        
        # Check if the GET request renders the availableteam page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'availableteam.html')

        # Check if the context contains all teams
        self.assertIn('teams', response.context)
        self.assertEqual(list(response.context['teams']), list(team.objects.all()))

    def test_add_team_page_shows_existing_teams(self):
        # Create a team to test if it appears on the page
        team.objects.create(name='Existing Team')
        response = self.client.get(self.url)

        self.assertContains(response, 'Existing Team')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'availableteam.html')
        self.assertIn('teams', response.context)
        self.assertEqual(len(response.context['teams']), 1)








