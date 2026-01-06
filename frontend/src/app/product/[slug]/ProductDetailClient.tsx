'use client'

import React, { useState } from 'react';
import { Product, Variant } from '@/components/ProductCard';
import { useCartStore } from '@/store/cartStore';
import { getVariantPriceStats } from '@/utils/productHelpers';

interface Props {
    product: Product;
}

export default function ProductDetailClient({ product }: Props) {

    const [selectedVariant, setSelectedVariant] = useState<Variant | null>(
        product.variants && product.variants.length > 0 ? product.variants[0] : null
    );

    const addToCart = useCartStore((state) => state.addToCart);
    const { minFinalPrice, maxOriginalPrice } = getVariantPriceStats(product.variants);

    return (
        <div className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Cột Trái: Ảnh */}
            <div className="bg-gray-100 rounded-lg h-96 relative">
                 {/* ... Code hiển thị ảnh ... */}
                 <p className="text-center pt-10">Ảnh sản phẩm ở đây</p>
            </div>

            {/* Cột Phải: Thông tin & Nút bấm */}
            <div>
                <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
                
                {/* Hiển thị giá */}
                <div className="flex gap-4 items-end mb-6">
                     <span className="text-3xl font-bold text-red-600">
                        {selectedVariant 
                            ? Number(selectedVariant.final_price).toLocaleString('vi-VN') 
                            : minFinalPrice.toLocaleString('vi-VN')} đ
                     </span>
                     {/* Gạch giá cũ nếu có */}
                </div>

                {/* Chọn Variant (Ví dụ logic) */}
                <div className="mb-6">
                    <h3 className="font-semibold mb-2">Chọn loại:</h3>
                    <div className="flex gap-2">
                        {product.variants.map((v) => (
                            <button
                                key={v.id}
                                onClick={() => setSelectedVariant(v)}
                                className={`px-4 py-2 border rounded ${
                                    selectedVariant?.id === v.id 
                                    ? 'border-blue-500 bg-blue-50 text-blue-700' 
                                    : 'border-gray-200 hover:border-gray-400'
                                }`}
                            >
                                {v.sku} {/* Hoặc hiển thị màu/size */}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Nút Mua */}
                <button 
                    onClick={() => {
                        if(selectedVariant) {
                            // Logic add to cart với variant cụ thể
                            alert(`Đã thêm: ${product.name} - ${selectedVariant.sku}`);
                        }
                    }}
                    className="w-full bg-blue-600 text-white py-4 rounded-lg font-bold hover:bg-blue-700"
                >
                    THÊM VÀO GIỎ
                </button>

                <div className="mt-8 prose">
                    <h3 className="font-semibold">Mô tả:</h3>
                    <p>{product.description}</p>
                </div>
            </div>
        </div>
    );
}