from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg,F,ExpressionWrapper
from django.db import models



@receiver(post_save, sender='App.PurchaseOrder')
def update_vendor_metrics_on_save(sender, instance, created, **kwargs):
    from .models import PurchaseOrder
    if created:  # Check if the instance was just created
        return  # Skip updating metrics for newly created instances

    vendor = instance.vendor

    # Update on-time delivery rate
    if instance.status == 'completed' :
        completed_pos_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_deliveries_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=F('promised_delivery_date')).count()
        if completed_pos_count > 0:      
            vendor.on_time_delivery_rate = (on_time_deliveries_count / completed_pos_count) * 100
            vendor.save()

    # Update quality rating average
    if instance.status == 'completed' and instance.quality_rating is not None:
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        if completed_pos.exists():
            avg_quality_rating = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
            vendor.quality_rating_avg = avg_quality_rating
            vendor.save()

    # Update average response time if acknowledgment date is updated
    if instance.acknowledgment_date:
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        if completed_pos.exists():
            avg_response_time_minutes = completed_pos.aggregate(
                avg_response_time=Avg(ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=models.DurationField()))
            )['avg_response_time'].total_seconds() / 60  # Convert timedelta to minutes
            vendor.average_response_time = abs(avg_response_time_minutes)
            vendor.save()


    # Update fulfillment rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    if total_pos.exists():
        fulfilment_rate = (completed_pos.count() / total_pos.count()) * 100
        vendor.fulfillment_rate = fulfilment_rate
        vendor.save()



@receiver(post_delete, sender='App.PurchaseOrder')
def update_vendor_metrics_on_delete(sender, instance, **kwargs):   
    from .models import PurchaseOrder
    vendor = instance.vendor
    # Update fulfillment rate after delete
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    if total_pos.exists():
        fulfilment_rate = (completed_pos.count() / total_pos.count()) * 100
        vendor.fulfillment_rate = fulfilment_rate
    else:
        vendor.fulfillment_rate = 0

    # Update quality rating average after delete
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    if completed_pos.exists():
        avg_quality_rating = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = avg_quality_rating
    else:
        vendor.quality_rating_avg = 0

    # Update average response time after delete
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    if completed_pos.exists():
        avg_response_time_minutes = completed_pos.aggregate(
            avg_response_time=Avg(ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=models.DurationField()))
        )['avg_response_time'].total_seconds() / 60  # Convert timedelta to minutes
        vendor.average_response_time = abs(avg_response_time_minutes)
    else:
        vendor.average_response_time = 0

    # Update on-time delivery rate after delete
    completed_pos_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    on_time_deliveries_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=F('promised_delivery_date')).count()
    if completed_pos_count > 0:      
        vendor.on_time_delivery_rate = (on_time_deliveries_count / completed_pos_count) * 100
    else:
        vendor.on_time_delivery_rate = 0

    vendor.save()

    
