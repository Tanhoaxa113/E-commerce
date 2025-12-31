import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.products.models import Product, ProductVariant, Category, Brand # Sửa lại import theo đúng project của muội
import shortuuid

class Command(BaseCommand):
    help = 'Tạo dữ liệu giả cho Shop Đồ Điện Tử (iPhone, Laptop...)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Đang khởi động máy in sản phẩm...'))

        # 1. Tạo Brands (Thương hiệu)
        brands = ['Apple', 'Samsung', 'Dell', 'Asus', 'Sony', 'Logitech']
        brand_objs = {}
        for b_name in brands:
            brand, _ = Brand.objects.get_or_create(name=b_name)
            brand_objs[b_name] = brand
        
        self.stdout.write(f'✅ Đã tạo {len(brands)} thương hiệu.')

        # 2. Tạo Categories (Danh mục)
        categories_data = {
            'Smartphone': 'Điện thoại thông minh, flagship',
            'Laptop': 'Máy tính xách tay, workstation',
            'Accessories': 'Phụ kiện, tai nghe, chuột'
        }
        cat_objs = {}
        for c_name, desc in categories_data.items():
            cat, _ = Category.objects.get_or_create(name=c_name)
            cat_objs[c_name] = cat
        
        self.stdout.write(f'✅ Đã tạo {len(categories_data)} danh mục.')

        # 3. List sản phẩm mẫu (Data xịn)
        products_list = [
            # Smartphone
            {
                'name': 'iPhone 15 Pro Max', 'brand': 'Apple', 'cat': 'Smartphone',
                'desc': 'Titanium tự nhiên, Chip A17 Pro mạnh mẽ nhất.',
                'variants': [
                    {'sku': 'IP15PM-256-NAT', 'name': '256GB / Titan Tự Nhiên', 'price': 29990000, 'stock': 10, 'specs': {'color': 'Natural Titanium', 'storage': '256GB', 'screen': '6.7 inch'}},
                    {'sku': 'IP15PM-512-BLU', 'name': '512GB / Titan Xanh', 'price': 34990000, 'stock': 5, 'specs': {'color': 'Blue Titanium', 'storage': '512GB', 'screen': '6.7 inch'}},
                    {'sku': 'IP15PM-1TB-BLK', 'name': '1TB / Titan Đen', 'price': 44990000, 'stock': 0, 'specs': {'color': 'Black Titanium', 'storage': '1TB', 'screen': '6.7 inch'}}, # Hết hàng để test case Failed
                ]
            },
            {
                'name': 'Samsung Galaxy S24 Ultra', 'brand': 'Samsung', 'cat': 'Smartphone',
                'desc': 'Quyền năng Galaxy AI, Camera mắt thần bóng đêm.',
                'variants': [
                    {'sku': 'S24U-256-GRY', 'name': '256GB / Xám Titan', 'price': 26990000, 'stock': 20, 'specs': {'color': 'Grey', 'storage': '256GB', 'ram': '12GB'}},
                    {'sku': 'S24U-512-YEL', 'name': '512GB / Vàng Amber', 'price': 31990000, 'stock': 15, 'specs': {'color': 'Yellow', 'storage': '512GB', 'ram': '12GB'}},
                ]
            },
            # Laptop
            {
                'name': 'MacBook Pro 14 M3', 'brand': 'Apple', 'cat': 'Laptop',
                'desc': 'Chip M3 Pro cân mọi tác vụ đồ họa.',
                'variants': [
                    {'sku': 'MBP14-M3-18-512', 'name': 'M3 Pro / 18GB RAM / 512GB', 'price': 49990000, 'stock': 8, 'specs': {'cpu': 'M3 Pro', 'ram': '18GB', 'ssd': '512GB'}},
                    {'sku': 'MBP14-M3-36-1TB', 'name': 'M3 Max / 36GB RAM / 1TB', 'price': 79990000, 'stock': 3, 'specs': {'cpu': 'M3 Max', 'ram': '36GB', 'ssd': '1TB'}},
                ]
            },
            {
                'name': 'Dell XPS 13 Plus', 'brand': 'Dell', 'cat': 'Laptop',
                'desc': 'Thiết kế tương lai, màn hình OLED 4K.',
                'variants': [
                    {'sku': 'XPS13-I7-16', 'name': 'Core i7 / 16GB / 512GB', 'price': 45000000, 'stock': 12, 'specs': {'cpu': 'Intel Core i7', 'ram': '16GB', 'screen': '13.4 OLED'}},
                ]
            },
             # Phụ kiện
            {
                'name': 'Sony WH-1000XM5', 'brand': 'Sony', 'cat': 'Accessories',
                'desc': 'Tai nghe chống ồn chủ động tốt nhất thế giới.',
                'variants': [
                    {'sku': 'SONY-XM5-BLK', 'name': 'Màu Đen', 'price': 7490000, 'stock': 50, 'specs': {'color': 'Black', 'type': 'Over-ear'}},
                    {'sku': 'SONY-XM5-SLV', 'name': 'Màu Bạc', 'price': 7490000, 'stock': 30, 'specs': {'color': 'Silver', 'type': 'Over-ear'}},
                ]
            },
        ]

        # 4. Loop tạo sản phẩm
        for p_data in products_list:
            # Tạo Product cha
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'slug': slugify(p_data['name']),
                    'description': p_data['desc'],
                    'category': cat_objs[p_data['cat']],
                    'brand': brand_objs[p_data['brand']],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f"✨ Đã tạo: {product.name}")
            else:
                self.stdout.write(f"⚠️ Đã có: {product.name}")

            # Tạo Variants con
            for v_data in p_data['variants']:
                VariantModel = ProductVariant 
                # Lưu ý: Muội check lại tên Model Variant của muội nhé
                
                v, v_created = VariantModel.objects.get_or_create(
                    sku=v_data['sku'],
                    defaults={
                        'product': product,
                        'name': v_data['name'], # Tên hiển thị variant
                        'price': v_data['price'],
                        'price': v_data['price'] * 1.2, # Giá thị trường cao hơn xíu để hiện giảm giá
                        'variant_specs': v_data['specs'], # JSON Field
                        'is_active': True
                    }
                )

        self.stdout.write(self.style.SUCCESS('\n🎉 Xong.'))