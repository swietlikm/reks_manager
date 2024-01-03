# import json
#
# from django.test import Client, TestCase
# from django.urls import reverse
# from django.utils import timezone
# from django.utils.translation import gettext as _
# from rest_framework import status
# from rest_framework.authtoken.models import Token
#
# from reks_manager.users.models import User
# from .models import ALLERGY_CATEGORY, Allergy
# from .serializers import AllergiesSerializer
#
#
# class AllergyModelTest(TestCase):
#     """Test cases for the Allergy model."""
#
#     def setUp(self):
#         """Set up data for the test cases."""
#
#         # Create an instance of Allergy for testing
#         self.allergy_data = {
#             "category": ALLERGY_CATEGORY[0][0],
#             "name": "Peanut Allergy",
#             "description": "Allergic to peanuts",
#         }
#
#         self.allergy_instance = Allergy.objects.create(**self.allergy_data)
#
#     def test_allergy_creation(self):
#         """Test the creation of an allergy instance."""
#
#         # Assert statements to verify the created instance's attributes
#         self.assertEqual(self.allergy_instance.category, self.allergy_data["category"])
#         self.assertEqual(self.allergy_instance.name, self.allergy_data["name"])
#         self.assertEqual(self.allergy_instance.description, self.allergy_data["description"])
#         self.assertIsInstance(self.allergy_instance.created_at, timezone.datetime)
#         self.assertIsInstance(self.allergy_instance.updated_at, timezone.datetime)
#         self.assertEqual(
#             str(self.allergy_instance), _("Allergy") + f": {self.allergy_data['category']} {self.allergy_data['name']}"
#         )
#
#     def test_allergy_unique_together_constraint(self):
#         """Test the unique together constraint for allergies."""
#
#         # Attempt to create a duplicate instance and assert it raises an exception
#         allergy2_data = {
#             "category": self.allergy_data["category"],
#             "name": self.allergy_data["name"],
#             "description": "Another description",
#         }
#         with self.assertRaises(Exception):
#             Allergy.objects.create(**allergy2_data)
#
#     def test_allergy_create(self):
#         """Test creating an allergy instance."""
#         allergies_count = Allergy.objects.count()
#
#         allergy2_data = {
#             "category": ALLERGY_CATEGORY[1][0],
#             "name": "other name",
#             "description": "Another description",
#         }
#         allergy2 = Allergy.objects.create(**allergy2_data)
#
#         self.assertEqual(self.allergy_instance.category, self.allergy_data["category"])
#         self.assertEqual(self.allergy_instance.name, self.allergy_data["name"])
#         self.assertEqual(self.allergy_instance.description, self.allergy_data["description"])
#
#         self.assertEqual(allergy2.category, allergy2_data["category"])
#         self.assertEqual(allergy2.name, allergy2_data["name"])
#         self.assertEqual(allergy2.description, allergy2_data["description"])
#
#         self.assertEqual(Allergy.objects.count(), allergies_count + 1)
#
#     def test_allergy_update(self):
#         """Test updating an allergy instance."""
#
#         updated_description = "Updated description"
#         self.allergy_data["description"] = updated_description
#
#         allergy = Allergy.objects.get(pk=self.allergy_instance.pk)
#         allergy.description = updated_description
#         allergy.save()
#
#         updated_allergy = Allergy.objects.get(pk=self.allergy_instance.pk)
#         self.assertEqual(updated_allergy.description, updated_description)
#
#     def test_allergy_delete(self):
#         """Test deleting an allergy instance."""
#
#         allergy_count_before = Allergy.objects.count()
#         self.allergy_instance.delete()
#         allergy_count_after = Allergy.objects.count()
#
#         self.assertEqual(allergy_count_after, allergy_count_before - 1)
#
#
# class AllergiesSerializerTest(TestCase):
#     """Test cases for the AllergiesSerializer."""
#
#     def setUp(self):
#         """Set up data for the serializer test cases."""
#         self.allergy_data = {
#             "category": ALLERGY_CATEGORY[1][0],
#             "name": "Contact Dermatitis",
#             "description": "Skin allergy due to contact",
#         }
#         self.allergy_instance = Allergy.objects.create(**self.allergy_data)
#
#     def test_serializer_with_valid_data(self):
#         """Test the serializer with valid allergy data."""
#
#         serializer = AllergiesSerializer(instance=self.allergy_instance)
#         data = serializer.data
#         self.assertEqual(data["id"], self.allergy_instance.id)
#         self.assertEqual(data["category"], self.allergy_data["category"])
#         self.assertEqual(data["name"], self.allergy_data["name"])
#         self.assertEqual(data["description"], self.allergy_data["description"])
#
#     def test_serializer_with_empty_data(self):
#         """Test the serializer with empty data."""
#
#         serializer = AllergiesSerializer(data={})
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("category", serializer.errors)
#         self.assertIn("name", serializer.errors)
#
#     def test_serializer_with_only_category(self):
#         """Test the serializer with only the category."""
#
#         serializer = AllergiesSerializer(data={"category": ALLERGY_CATEGORY[0][0]})
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("name", serializer.errors)
#
#     def test_serializer_with_only_name(self):
#         """Test the serializer with only the name."""
#
#         serializer = AllergiesSerializer(data={"name": "something"})
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("category", serializer.errors)
#
#     def test_serializer_with_fake_category(self):
#         """Test the serializer with a fake category."""
#
#         serializer = AllergiesSerializer(data={"category": "FAKE_CATEGORY"})
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("category", serializer.errors)
#         self.assertIn("name", serializer.errors)
#
#
# class AllergyViewTest(TestCase):
#     """Test cases for allergy views."""
#
#     def setUp(self):
#         """Set up data for the view test cases."""
#
#         # Create a user
#         self.user = User.objects.create_user(email="test@test.test", password="testpassword", is_staff=True)
#
#         # Create a token for the user
#         self.token = Token.objects.create(user=self.user)
#
#         # Set up the client with the token in the Authorization header
#         self.client = Client(headers={"authorization": f"Token {self.token.key}"})
#
#         self.allergy_data = {
#             "category": ALLERGY_CATEGORY[0][0],
#             "name": "Peanut Allergy",
#             "description": "Allergic to peanuts",
#         }
#         self.allergy = Allergy.objects.create(**self.allergy_data)
#
#     def test_create_allergy_view(self):
#         """Test creating an allergy via the API."""
#         url = reverse("api:allergy-list")
#
#         # Send a POST request to create a new allergy
#         response = self.client.post(
#             url, data={"category": ALLERGY_CATEGORY[0][0], "name": "NewName", "description": "NewDescription"}
#         )
#
#         # Check if the response is successful (status code 200) or redirect (status code 302)
#         self.assertIn(response.status_code, [200, 201, 302])
#
#         # Optionally, check if the allergy was created in the database
#         new_allergy = Allergy.objects.get(name="NewName")
#         self.assertIsNotNone(new_allergy)
#
#     def test_update_allergy_view(self):
#         """Test updating an allergy via the API."""
#
#         # create test instance
#         allergy_data = {
#             "category": ALLERGY_CATEGORY[0][0],
#             "name": "Some Allergy",
#             "description": "Some Description",
#         }
#         allergy = Allergy.objects.create(**allergy_data)
#         url = reverse("api:allergy-detail", kwargs={"pk": allergy.pk})
#
#         allergy_data2 = {
#             "category": ALLERGY_CATEGORY[1][0],
#             "name": "Some Allergy updated",
#             "description": "Some Description UPDATED",
#         }
#         # Send a POST request to update the allergy
#         response = self.client.put(url, data=json.dumps(allergy_data2), content_type="application/json")
#
#         # Check if the response is successful (status code 200) or redirect (status code 302)
#         self.assertIn(response.status_code, [200, 302])
#
#         # Check if the allergy was updated in the database with PUT
#         updated_allergy = Allergy.objects.get(pk=allergy.pk)
#         self.assertEqual(updated_allergy.name, "Some Allergy updated")
#         self.assertEqual(updated_allergy.description, "Some Description UPDATED")
#
#         # Check if the allergy was updated in the database with PATCH
#         response = self.client.patch(url, data={"description": "lol"}, content_type="application/json")
#         self.assertIn(response.status_code, [200, 302])
#         updated_allergy = Allergy.objects.get(pk=allergy.pk)
#         self.assertEqual(updated_allergy.description, "lol")
#
#     def test_delete_allergy_view(self):
#         """Test deleting an allergy via the API."""
#         url = reverse("api:allergy-detail", kwargs={"pk": self.allergy.pk})
#
#         # Send a DELETE request to delete the allergy
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Check if the allergy was deleted from the database
#         with self.assertRaises(Allergy.DoesNotExist):
#             Allergy.objects.get(pk=self.allergy.pk)
