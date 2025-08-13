import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.entities.order import Order, OrderStatus
from src.entities.order_item import OrderItem
from src.entities.order_item_extra import OrderItemExtra
from src.entities.food_item import FoodItem
from src.entities.extra import Extra
from . import models

def create_order(db: Session, order_create: models.OrderCreate) -> models.OrderResponse:
    try:
        # Collect all required IDs for bulk queries
        food_item_ids = [item.food_item_id for item in order_create.items]
        all_extra_ids = set()
        for item in order_create.items:
            all_extra_ids.update(item.extra_ids)
        
        # Bulk query all food items 
        food_items = db.query(FoodItem).filter(FoodItem.id.in_(food_item_ids)).all()
        food_items_dict = {str(food.id): food for food in food_items}
        
        # Check for missing food items
        missing_food_ids = set(str(fid) for fid in food_item_ids) - set(food_items_dict.keys())
        if missing_food_ids:
            raise HTTPException(
                status_code=404, 
                detail=f"Food items not found: {', '.join(missing_food_ids)}"
            )
        
        # Bulk query all extras
        extras_dict = {}
        if all_extra_ids:
            extras = db.query(Extra).filter(Extra.id.in_(all_extra_ids)).all()
            extras_dict = {str(extra.id): extra for extra in extras}
            
            # Check for missing extras
            missing_extra_ids = set(str(eid) for eid in all_extra_ids) - set(extras_dict.keys())
            if missing_extra_ids:
                raise HTTPException(
                    status_code=404,
                    detail=f"Extras not found: {', '.join(missing_extra_ids)}"
                )
        
        # Create the order
        order = Order(
            id=uuid.uuid4(),
            status=OrderStatus.CREATED,
            currency=order_create.currency,
            customer_name=order_create.customer_name,
            customer_address=order_create.customer_address,
            total_amount=Decimal('0'),
            created_at=datetime.now(timezone.utc)
        )
        db.add(order)
        db.flush()  # Get the order ID
        
        total_amount = Decimal('0')
        order_items_response = []
        order_items_to_add = []
        order_item_extras_to_add = []
        
        # Process each order item
        for item in order_create.items:
            food_item = food_items_dict[str(item.food_item_id)]
            
            # Calculate extras total
            extras_total = Decimal('0')
            extras_list = []
            
            # Process extras if any
            if item.extra_ids:
                for extra_id in item.extra_ids:
                    extra = extras_dict[str(extra_id)]
                    extras_total += extra.price
                    extras_list.append(extra)
            
            # Calculate line total
            unit_price = food_item.base_price + extras_total
            line_total = unit_price * item.quantity
            total_amount += line_total
            
            # Create order item
            order_item = OrderItem(
                id=uuid.uuid4(),
                order_id=order.id,
                food_item_id=food_item.id,
                quantity=item.quantity,
                unit_price=unit_price
            )
            order_items_to_add.append(order_item)
            
            # Prepare order item extras
            for extra in extras_list:
                order_item_extra = OrderItemExtra(
                    order_item_id=order_item.id,
                    extra_id=extra.id,
                    extra_price=extra.price
                )
                order_item_extras_to_add.append(order_item_extra)
            
            # Build response item
            order_items_response.append({
                'food_item_id': food_item.id,
                'food_item_name': food_item.name,
                'quantity': item.quantity,
                'unit_price': str(unit_price),
                'extras': [{'id': e.id, 'name': e.name, 'price': str(e.price)} for e in extras_list],
                'line_total': str(line_total)
            })
        
        # Bulk add all order items
        db.add_all(order_items_to_add)
        db.flush()  # Get order item IDs
        
        # Bulk add all order item extras
        if order_item_extras_to_add:
            db.add_all(order_item_extras_to_add)
        
        # Update order total
        order.total_amount = total_amount
        
        # Commit the entire transaction
        db.commit()
        
        # Build full response
        return models.OrderResponse(
            id=order.id,
            status=order.status.value,
            currency=order.currency.value,
            customer_name=order.customer_name,
            customer_address=order.customer_address,
            items=[
                models.OrderItemResponse(
                    food_item_id=item['food_item_id'],
                    food_item_name=item['food_item_name'],
                    quantity=item['quantity'],
                    unit_price=Decimal(item['unit_price']),
                    extras=[
                        models.ExtraInResponse(
                            id=extra['id'],
                            name=extra['name'],
                            price=Decimal(extra['price'])
                        ) for extra in item['extras']
                    ],
                    line_total=Decimal(item['line_total'])
                ) for item in order_items_response
            ],
            total_amount=order.total_amount,
            created_at=order.created_at.isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions without rollback (they're expected)
        raise
    except Exception as e:
        # Rollback on any other exception
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create order: {str(e)}"
        )
