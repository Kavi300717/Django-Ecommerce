from django.core.management.base import BaseCommand
from store.models import Product, Variation

class Command(BaseCommand):
    help = 'Add sample size and color variations to all products'

    def handle(self, *args, **options):
        colors = ['Gray', 'Black']
        sizes = ['Small', 'Medium', 'Large', 'Extra Large']
        
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.WARNING('No products found in database'))
            return
        
        variation_count = 0
        
        for product in products:
            # Add color variations
            for color in colors:
                variation, created = Variation.objects.get_or_create(
                    product=product,
                    variation_category='color',
                    variation_value=color,
                    defaults={'is_active': True}
                )
                if created:
                    variation_count += 1
                    self.stdout.write(f'Added: {product.product_name} - Color: {color}')
            
            # Add size variations
            for size in sizes:
                variation, created = Variation.objects.get_or_create(
                    product=product,
                    variation_category='size',
                    variation_value=size,
                    defaults={'is_active': True}
                )
                if created:
                    variation_count += 1
                    self.stdout.write(f'Added: {product.product_name} - Size: {size}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {variation_count} variations'))
