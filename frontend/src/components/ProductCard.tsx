'use client'
import React from "react"
import Image from 'next/image'
import { useCartStore } from '@/store/cartStore';
import { useRouter } from "next/navigation";

export interface Variants{
    id: string
    sku: string
    price: string
    final_price: string
    discount_rate: number
    variant_specs: any

}
export interface Product {
    id: string
    name: string
    slug: string
    description: string
    variants: Variants[]
}

interface ProductCardProps {
    product: Product
}


const ProductCard = ({ product }: ProductCardProps) => {
    const addToCart = useCartStore((state) => state.addToCart);
    const router = useRouter()

    const formatPrice = (price: number) => {
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND"
        }).format(price)
    }

    const handleProductClick = (event: React.MouseEvent) => {
        router.push(`/product/${product.slug}`)
    }

    // 2. Logic lấy giá hiển thị
    // Lấy biến thể đầu tiên làm đại diện
    const displayVariant = product.variants && product.variants.length > 0 ? product.variants[0] : null;
    
    // Ép kiểu từ string sang number
    const displayPrice = displayVariant ? Number(displayVariant.final_price) : 0;

    return (
        <div onClick={handleProductClick} className="border border-gray-200 rounded-lg p-4 bg-white hover:shadow-lg transition-shadow cursor-pointer group" >
            <div className="relative w-full h-48 border-gray-200 rounder-md mb-4 flex items-center text-gray-400">
                <Image
                    src={`https://placehold.co/400x400?text=${product.name}`}
                    alt={product.name}
                    fill
                    className="object-cover rounded-md transition-transform group-hover:scale-105"
                    unoptimized={true}
                />
            </div>
            <h3 className="font-semibold text-lg text-gray-700 truncate group-hover:text-blue-600 transition-colors">
                {product.name}
            </h3>
            
            <p className="text-red-500 font-bold mt-2">
                {/* 3. Hiển thị giá */}
                {displayVariant ? formatPrice(displayPrice) : "Liên hệ"}
            </p>

            <button
                onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    // Lưu ý: Chỗ này muội cũng cần sửa addToCart để nhận đúng Variant nhé
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