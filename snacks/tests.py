from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Snack
from django.urls import reverse

# Create your tests here.

class Snacktest(TestCase) :
    def setUp(self) :
        self.user = get_user_model().objects.create_user(
            username='Ibrahim',
            email='Ibrahim@Ibrahim.com',
            password='Ibrahim@81'
        )

        self.snack = Snack.objects.create(
            name='test',
            purchaser= self.user,
            desc='test description'
        )

    def test_str_method(self):
        expected_string = "test"  # Replace with the expected string representation of your Snack object
        self.assertEqual(str(self.snack), expected_string)

    def test_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "snack_list.html")

    def test_detail_view(self):
            url = reverse('snack_detail',args=[self.snack.id])  
            response = self.client.get(url)

            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed(response,'snack_detail.html')


    def test_create_view(self):
        url = reverse('snack_create')
        data={
            "name": "test_2",
            "purchaser" : self.user.id,
            "desc": 'test_02'
        }


        response = self.client.post(path=url,data = data,follow = True)
        self.assertTemplateUsed(response,'snack_detail.html')
        self.assertEqual(len(Snack.objects.all()),2)
        self.assertRedirects(response, reverse('snack_detail',args=[2]))

    def test_update_view(self):
       
        response = self.client.post(reverse('snack_update',args="1"),
                    {"name": "Updated name", "desc": "description", "purchaser": self.user.id})
        
        self.assertRedirects(response, reverse('snack_list'))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)