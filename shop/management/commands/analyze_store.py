from django.core.management.base import BaseCommand
from django.db.models import Count, Max, Min, Avg, Sum, Q
from shop.models import Category, Item

class Command(BaseCommand):
    help = 'Analyze store data using Django ORM'

    def handle(self, *args, **kwargs):
        total_items = Category.objects.aggregate(
            total_items=Count('items'),
            max_price=Max('items__price'),
            min_price=Min('items__price'),
            avg_price = Avg('items__price')
        )

        print(f"Total Items: {total_items}")

        # ---------------------------------------------------------------------------------------------------------------------------------------------

        categories = Category.objects.annotate(
            items_count = Count('items'),
            items_price = Sum('items__price', default=0)
        )

        for category in categories:
            print(f"{category.name}, item_count: {category.items_count}, item_price: {category.items_price}")


        # ---------------------------------------------------------------------------------------------------------------------------------------------
            
        items = Item.objects.select_related('category')

        for item in items:
            print(f"Item: {item.name}, Category: {item.category.name}")

        # ---------------------------------------------------------------------------------------------------------------------------------------------
        
        items = Item.objects.prefetch_related('tags')

        for item in items:
            tag_names = [tag.name for tag in item.tags.all()]  
            print(f"Item: {item.name}, Tags: {', '.join(tag_names)}")

        
        