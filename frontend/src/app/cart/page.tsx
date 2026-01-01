'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

import { useCartStore } from '@/store/cartStore';

const CartPage = () => {
    const {addToCart, cart, removeFromCart, decreaseQuantity, clearCart} = useCartStore();
    const totalPrice = cart.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);

    const formatPrice = (price: number) => 
        new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);

    if (cart.length === 0){
        return (
            <div className="p-10 text-center text-gray-500">
                <div className="p-10 text-center text-gray-500">
                    Chưa có gì
                    <br />
                    <Link href="/" className="text-blue-500 underline">Quay lại mua sắm</Link>
                </div>
            </div>
        )
    }
    return (
        <div className="container mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cột trái: Danh sách hàng */}
            <div className="lg:col-span-2 space-y-4">
                <h1 className="text-2xl font-bold mb-6">Giỏ hàng</h1>
                
                {/* TODO 4: Dùng hàm .map() để render danh sách sản phẩm 
                   Thay cái mảng rỗng [] bằng biến cart
                */}
                {cart.map((item) => (
                    <div key={item.id} className="flex gap-4 p-4 border rounded-lg bg-white items-center">
                        {/* Ảnh */}
                        <div className="relative w-20 h-20">
                            <Image 
                                src={`https://placehold.co/200x200?text=${item.name}`} 
                                alt={item.name} 
                                fill 
                                className="object-cover rounded"
                                unoptimized
                            />
                        </div>

                        {/* Thông tin */}
                        <div className="flex-1">
                            <h3 className="font-bold">{item.name}</h3>
                            <p className="text-sm text-gray-500">{formatPrice(item.price)}</p>
                        </div>

                        {/* Bộ điều khiển */}
                        <div className="flex items-center gap-3">
                            {/* TODO 5: Gắn sự kiện onClick cho nút TRỪ và CỘNG 
                               Nút -: Gọi decreaseQuantity(item.id)
                               Nút +: Gọi addToCart(item)
                            */}
                            <button 
                                onClick={() => decreaseQuantity(item.id)}
                                className="px-2 py-1 bg-gray-100 rounded"
                            >
                                -
                            </button>
                            <span>{item.quantity}</span>
                            <button 
                                onClick={() => {addToCart(item)}}
                                className="px-2 py-1 bg-gray-100 rounded"
                            >
                                +
                            </button>
                        </div>

                        {/* Nút xóa */}
                        <button 
                            onClick={() => removeFromCart(item.id)}
                            className="text-red-500 ml-4"
                        >
                            Xóa
                        </button>
                    </div>
                ))}
                <div className=''>
                    <button
                        onClick={() => {clearCart()}}
                        className='bg-red-600'> Xóa Giỏ Hàng </button>
                </div>
            </div>
            
            {/* Cột phải: Tính tiền */}
            <div className="bg-gray-50 p-6 rounded-xl h-fit border">
                <div className="flex justify-between mb-4 font-bold text-xl">
                    <span>Tổng cộng:</span>
                    {/* TODO 6: Hiển thị biến totalPrice đã format vào đây */}
                    <span>{formatPrice(totalPrice)}</span> 
                </div>
                <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700">
                    Thanh toán
                </button>
            </div>
        </div>
    );
};

export default CartPage;