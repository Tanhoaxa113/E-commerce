'use client'
import React from "react"
import Image from 'next/image'
import { useCartStore } from '@/store/cartStore';
import { useRouter } from "next/navigation";
export interface Product {
    id: string
    name: string
    price: number
    image: string
    slug: string
}

interface ProductCardProps {
    product: Product
}


const ProductCard = ({ product }: ProductCardProps) => {
    const addToCart = useCartStore((state) => state.addToCart);
    const formatPrice = (price: number) => {
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND"
        }).format(price)
    }
    const router = useRouter()
    const handleProductClick = (event: React.MouseEvent) => {
        router.push(`/product/${product.slug}`)
    }
    return (
        <div onClick={handleProductClick} className="border border-gray-200 rounded-lg p-4 bg-white hover:shadow-lg transition-shadow cursor-pointer" >
            <div className="relative w-full h-48 border-gray-200 rounder-md mb-4 flex items-center text-gray-400">
                <Image
                    src={`https://placehold.co/400x400?text=${product.name}`}
                    alt={product.name}
                    fill
                    className="object-cover rounded-md"
                    unoptimized={true}
                />
            </div>
            <h3 className="font-semibold text-lg text-gray-700 truncate">
                {product.name}
            </h3>
            <p className="text-red-500 font-bold mt-2">
                {formatPrice(product.price)}
            </p>
            <button
                onClick={(e) => {
                    // 🛑 LỆNH CẤM CỬA:
                    e.preventDefault();   // 1. Cấm thẻ Link (nếu có) thực hiện chuyển trang
                    e.stopPropagation();  // 2. Cấm sự kiện "mách lẻo" nổi lên thằng Cha (div)

                    // Logic của muội
                    addToCart(product);
                }}
                className="mt-4 w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors active:scale-95"
            >
                Thêm vào giỏ
            </button>
        </div>
    )
}
export default ProductCard;