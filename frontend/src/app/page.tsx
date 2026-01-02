import type { Metadata } from 'next'
import Link from 'next/link'
import ProductCard, { Product } from '@/components/ProductCard';

async function getProducts() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/products/`,{
    method: "GET",
    cache: 'no-store',
  })
  if (!res.ok){
    throw new Error("Không thể lấy danh sách")
  }
  return res.json()
}
export const metadata: Metadata = {
  title: 'Trang chủ | TTG Shop',
  description: 'Đây là trang chủ',
}

export default async function Home() {
  const products = await getProducts();
  console.log(products)
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
            {products.map((product: any) => (
              <ProductCard key={product.id} product={product} />
            ))}
        </div>
    </div>

  )
}