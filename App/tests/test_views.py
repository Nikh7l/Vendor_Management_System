from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from App.models import Vendor,PurchaseOrder
from App.views import generate_tokens
import subprocess

class VendorAPITests(APITestCase):
    def setUp(self):
        # Create a test vendor for use in tests
        self.vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "Test Address",
            "vendor_code": "TEST001"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        access_token, _ = generate_tokens()

        # Set up authentication headers with JWT access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_vendor(self):
        url = reverse('vendor')
        vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "Test Address",
            "vendor_code": "TEST002"
        }
        
        response = self.client.post(url, vendor_data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_vendors(self):
        url = reverse('vendor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        updated_data = {
            "name": "Updated Vendor",
            "contact_details": "updated@test.com",
            "address": "Updated Address",
            "vendor_code": "UPDATED001"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        # Create a test vendor for use in tests
        self.vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "Test Address",
            "vendor_code": "TEST001"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        # Create a test purchase order for use in tests
        self.purchase_order_data = {
            "po_number": "PO001",
            "vendor": self.vendor,
            "order_date": "2024-05-01",
            "promised_delivery_date": "2024-05-10",
            "items": [{"name": "Item 1", "quantity": 5}],
            "quantity": 5,
            "status": "pending",
            "issue_date": "2024-05-01T10:00:00Z"
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

        access_token, _ = generate_tokens()

        # Set up authentication headers with JWT access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_purchase_order(self):
        url = reverse('purchase_orders')
        purchase_order_data = {
            "po_number": "PO002",
            "vendor": self.vendor.pk,
            "order_date": "2024-05-01",
            "promised_delivery_date": "2024-05-10",
            "items": [{"name": "Item 1", "quantity": 5}],
            "quantity": 5,
            "status": "pending",
            "issue_date": "2024-05-01T10:00:00Z"
        }
        response = self.client.post(url, purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_purchase_orders(self):
        url = reverse('purchase_orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase_order_detail', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse('purchase_order_detail', args=[self.purchase_order.id])
        updated_data = {
            "delivery_date":"2024-05-08",
            "status": "completed",
            "quality_rating": 4.5
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse('purchase_order_detail', args=[self.purchase_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge_purchase_order', args=[self.purchase_order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vendor_performance(self):
        url = reverse('vendor_performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
