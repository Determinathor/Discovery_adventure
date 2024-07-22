from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from viewer.views import Order, Order_Line, Product


# @receiver(post_save, sender=Order)
# def update_stock(sender, instance, **kwargs):
#     if instance.status == 'Confirmed':
#         order_lines = instance.order_line_set.all()
#         for line in order_lines:
#             product = line.Product
#             if product.stock >= line.quantity:
#                 product.stock -= line.quantity
#                 product.save()
#             else:
#                 raise ValueError(f"Insufficient stock for {product.title}")