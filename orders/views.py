import json
import uuid
from datetime    import date 

from django.http    import JsonResponse
from django.views   import View
from django.db      import transaction

from orders.models   import Cart, Order, OrderItem, OrderStatus, ItemStatus, Coupon
from products.models import Option
from accounts.utils  import user_validator
from orders.response import orders_schema_dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CartView(APIView):
    @swagger_auto_schema(manual_parameters = [], responses = orders_schema_dict)
    @user_validator
    def post(self, request):
        try:
            data          = json.loads(request.body)
            
            option = Option.objects.get(id=data['option_id'])

            if option.stocks <= 0:
                return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            cart, created = Cart.objects.get_or_create(account=request.user, option=option)
            
            if not created:
                if cart.quantity + 1 > option.stocks:
                    return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

                cart.quantity += 1
                cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

        except Option.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION_ID"}, status=404)

    @swagger_auto_schema(manual_parameters = [], responses = orders_schema_dict)
    @user_validator
    def get(self, request):
        carts = Cart.objects.filter(account=request.user)

        results = {
            'carts': [
                {
                    "product_name"        : cart.option.product.name,
                    "thumbnail_image_url" : cart.option.product.thumbnail_image_url,
                    "product_id"          : cart.option.product_id,
                    "option_id"           : cart.option.id,
                    "weight"              : cart.option.weight,
                    "price"               : float(cart.option.price),
                    "quantity"            : cart.quantity,
                    "stocks"              : cart.option.stocks,
                    "availability"        : (cart.option.stocks >= cart.quantity)
                } for cart in carts],
            'total': sum(cart.quantity for cart in carts)
        }

        return JsonResponse({"results": results}, status=200)

    @user_validator
    def patch(self, request, option_id):
        try:
            data = json.loads(request.body)

            if data['quantity'] <= 0:
                return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            cart = Cart.objects.get(account=request.user, option_id=option_id)

            if data['quantity'] > cart.option.stocks:
                return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            cart.quantity = data['quantity']
            cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=404)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400) 

        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "JSON_ERROR"}, status=400)

    @user_validator
    def delete(self, request, option_id):
        try:
            cart = Cart.objects.get(account=request.user, option_id=option_id)
            cart.delete()

            return JsonResponse({"message": "SUCCESS"}, status=204)
        
        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=404)

class OrderView(View):
    @user_validator
    def post(self, request):
        try:
            carts = Cart.objects.filter(account=request.user)

            if not carts.exists():
                return JsonResponse({"message": "EMPTY_CART"}, status=400)

            for cart in carts:
                if cart.quantity > cart.option.stocks:
                    return JsonResponse({"messeage": "INVALID_QUANTITY"}, status=400)

            with transaction.atomic():
                order = Order.objects.create(
                    account      = request.user,
                    order_number = uuid.uuid4(),
                    status       = OrderStatus.objects.get(name="Pending")
                )

                for cart in carts:
                    OrderItem.objects.create(
                        order_id  = order.id,
                        option_id = cart.option.id,
                        quantity  = cart.quantity,
                        status    = ItemStatus.objects.get(name="Pending")
                    )

                    cart.option.stocks -= cart.quantity
                    cart.option.sales  += cart.quantity
                    cart.option.save()

                carts.delete()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except IndexError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER_STATUS"}, status=400)

        except ItemStatus.DoesNotExist:
            return JsonResponse({"message": "INVALID_ITEM_STATUS"}, status=400)

    @user_validator
    def get(self, request):
        orders  = Order.objects.filter(account=request.user).order_by('-ordered_at')
        
        results = [
            {
                "order_id"       : order.id,
                "order_number"   : order.order_number,
                "order_status"   : order.status.name,
                "ordered_at"     : order.ordered_at,
                "order_products" : [
                    {
                        "order_item_id"     : orderitem.id,
                        "product_id"        : orderitem.option.product_id,
                        "product_name"      : orderitem.option.product.name,
                        "product_image_url" : orderitem.option.product.thumbnail_image_url,
                        "quantity"          : orderitem.quantity,
                        "option_id"         : orderitem.option_id,
                        "weight"            : orderitem.option.weight,
                        "price"             : float(orderitem.option.price),
                        "item_status"       : orderitem.status.name
                    } for orderitem in order.orderitem_set.all()]
            } for order in orders]

        return JsonResponse({"results": results}, status=200)

    @user_validator
    def patch(self, request, order_id):
        try:
            data = json.loads(request.body)

            with transaction.atomic():
                order = Order.objects.get(id=order_id, account=request.user)

                order.status = OrderStatus.objects.get(name=data['order_status'])
                order.save()

                for order_item in data['order_items']:
                    item = order.orderitem_set.get(id=order_item['id'])

                    item.status = ItemStatus.objects.get(name=order_item['status'])
                    item.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER"}, status=404)

        except OrderItem.DoesNotExist:
            return JsonResponse({"message": "INVALID_ITEM"}, status=400)
        
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER_STATUS"}, status=400)

        except ItemStatus.DoesNotExist:
            return JsonResponse({"message": "INVALID_ITEM_STATUS"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class CouponView(View):
    def get(self, request, coupon_code):
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
            results = {
                'availability'     : date.today() < coupon.expiry_date,
                'discount_percent' : float(coupon.discount_percent),
                'discount_price'   : float(coupon.discount_price)
            }

            return JsonResponse({"results": results}, status=200)
        
        except Coupon.DoesNotExist:
            return JsonResponse({"message": "INVALID_COUPON"}, status=404)
