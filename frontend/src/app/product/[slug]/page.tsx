'use client'

import React from 'react'
import Image from 'next/image'
import Link from 'next/link'

import { useParams } from 'next/navigation'
import { useCartStore } from '@/store/cartStore';

const FAKE_PRODUCTS = [
    { id: "1a", slug: "vay-da-hoi", name: "Váy Dạ Hội", price: 500000, description: "Váy đẹp." },
    { id: "2x", slug: "ao-thun-coder", name: "Áo Thun Coder", price: 150000, description: "Mặc vào code không bao giờ bug." },
    { id: "3f", slug: "quan-short", name: "Quần Short", price: 200000, description: "Mát mẻ cho mùa hè." },
]

const ProductDetail = () => {
    const params = useParams(); 
    const currentSlug = params.slug; // Ví dụ: "vay-da-hoi-kim-sa"
    
    // Tìm sản phẩm theo SLUG chứ không theo ID nữa
    const product = FAKE_PRODUCTS.find(p => p.slug === currentSlug);

    if (!product) {
        return <div>Không tìm thấy sản phẩm nào có slug là: {currentSlug}</div>
    }
    const { addToCart } = useCartStore()

    return (
        <div className=''>
            <Link href="/" className='text-gray-500 hover:underline mb-4 block'>
                Quay lại mua sắm
            </Link>
            <div className='grid grid-cols-1 md:grid-cols-2 gap-10'>

                <div className='relative w-full h-[500px] bg-gray-100 rounded-xl overflow-hidden shadow-lg'>
                    <Image
                        src={`https://placehold.co/600x600?text=${product.name}`}
                        alt={product.name}
                        fill
                        className="object-cover"
                        unoptimized />
                </div>
                <div className="space-y-6">
                    <h1 className="text-4xl font-bold text-gray-800">{product.name}</h1>
                    <p className="text-2xl text-blue-600 font-semibold">
                        {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price)}
                    </p>

                    <div className="p-4 bg-gray-50 rounded-lg border">
                        <h3 className="font-bold mb-2">Mô tả sản phẩm:</h3>
                        <p className="text-gray-600 leading-relaxed">{product.description}</p>
                    </div>

                    <div className="flex gap-4 mt-8">
                        <button
                            onClick={() => addToCart({ ...product, image: '' })} // Tạm thời image rỗng
                            className="flex-1 bg-blue-600 text-white py-4 rounded-lg font-bold hover:bg-blue-700 transition transform active:scale-95 shadow-lg shadow-blue-500/30"
                        >
                            THÊM VÀO GIỎ NGAY
                        </button>
                        <button className="w-16 flex items-center justify-center border-2 border-gray-200 rounded-lg hover:bg-gray-50 text-2xl text-red-500">
                            ♥
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )

}

export default ProductDetail