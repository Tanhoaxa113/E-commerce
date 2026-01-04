'use client'
import React from "react"
import Image from 'next/image'
import { useCartStore } from '@/store/cartStore';
import { useRouter } from "next/navigation";
import { getVariantPriceStats } from '@/utils/productHelpers';
import { Product, ProductCardProps } from '@/app/types/Product';



const ProductCard = ({ product }: ProductCardProps) => {
    const addToCart = useCartStore((state) => state.addToCart);
    const router = useRouter()
    const { minFinalPrice, maxOriginalPrice } = getVariantPriceStats(product.variants);

    const formatPrice = (price: number) => {
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND"
        }).format(price)
    }

    const handleProductClick = (event: React.MouseEvent) => {
        router.push(`/product/${product.slug}`)
    }
    const displayVariant = product.variants && product.variants.length > 0 ? product.variants[0] : null;
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

            <div className="mt-2 text-blue-600 font-bold text-xl">
                {maxOriginalPrice > minFinalPrice && (
                    <span className="text-gray-400 line-through text-sm">
                        {formatPrice(maxOriginalPrice)}
                    </span>
                )}
                <span className="text-red-600 font-bold text-lg">
                    {formatPrice(minFinalPrice)}
                </span>
            </div>

            <button
                onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
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