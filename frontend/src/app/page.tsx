import type { Metadata } from 'next'
import Link from 'next/link'
import ProductCard, { Product } from '@/components/ProductCard';

const dummyProducts: Product[] = [
    { id: "1a", slug: "vay-da-hoi", name: "Váy Dạ Hội", price: 500000, image: "Váy đẹp." },
    { id: "2x", slug: "ao-thun-coder", name: "Áo Thun Coder", price: 150000, image: "Mặc vào code không bao giờ bug." },
    { id: "3f", slug: "quan-short", name: "Quần Short", price: 200000, image: "Mát mẻ cho mùa hè." },
];

export const metadata: Metadata = {
  title: 'Trang chủ | TTG Shop',
  description: 'Đây là trang chủ',
}

export default function Home() {
  return (
    <div>
        {/* Banner quảng cáo (Jumbotron) */}
        <div className="bg-blue-100 p-10 rounded-xl mb-8 text-center">
            <h1 className="text-4xl font-bold text-blue-800 mb-2">Siêu Sale Mùa Code</h1>
            <p className="text-blue-600">Giảm giá 50% cho lập trình viên thức khuya!</p>
        </div>

        {/* Danh sách sản phẩm */}
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Sản phẩm nổi bật</h2>
        
        {/* Lưới sản phẩm (Grid) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {dummyProducts.map((item) => (
                <ProductCard key={item.id} product={item} />
            ))}
        </div>
    </div>

  )
}