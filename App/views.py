from rest_framework import status
from rest_framework.response import Response
from .models import Vendor,PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime


@api_view(['POST','GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vendor(request):
    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data,partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def purchase_orders(request):
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if 'vendor_id' in request.GET:
            purchase_orders = PurchaseOrder.objects.filter(vendor=request.GET['vendor_id'])
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


from django.utils import timezone

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    purchase_order.acknowledgment_date = timezone.now()  
    purchase_order.save()

    return Response({'message': 'Purchase order acknowledged successfully'})




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Calculate performance metrics
    on_time_delivery_rate = vendor.on_time_delivery_rate
    quality_rating_avg = vendor.quality_rating_avg
    average_response_time = vendor.average_response_time
    fulfillment_rate = vendor.fulfillment_rate

    performance_data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    }

    return Response(performance_data)


##################################################################################################################
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens():
    # Check if the test user already exists
    if not User.objects.filter(username='test_user').exists():
        # Create a new user with username 'test_user' and password 'test_password'
        User.objects.create_user(username='test_user', password='test_password')

    # Retrieve the test user
    test_user = User.objects.get(username='test_user')

    # Generate tokens for the test user
    refresh = RefreshToken.for_user(test_user)

    # Return the generated tokens
    return str(refresh.access_token), str(refresh)