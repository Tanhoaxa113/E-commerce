'use client'

import { useCartStore } from '@/store/cartStore'
import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

const CheckoutPage = () => {
    const { cart, clearCart } = useCartStore()
    const router = useRouter()

    const [formData, setFormData] = useState({
        fullName: '',
        phone: '',
        address: '',
        note: '',
    })

    const [isLoading, setIsLoading] = useState(false)
    const totalPrice = cart.reduce((total, item) => total + item.price * item.quantity, 0)
    const formatPrice = (price: number) => {
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND"
        }).format(price)
    }
    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };
    const handleOrder = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (cart.length === 0) {
            alert("Gio hang trong")
            return;
        }
        setIsLoading(true)
        try {
            await new Promise(resolve => setTimeout(resolve, 2000));

            const orderData = {
                fullName: formData.fullName,
                phone: formData.phone,
                address: formData.address,
                note: formData.note,
                items: cart.map(item => ({
                    id: item.id,
                    name: item.name,
                    price: item.price,
                    quantity: item.quantity,
                })),
                total: totalPrice,
            }
            console.log(orderData)

            alert("Dat hang thanh cong")
            clearCart()
            router.push("/")
        } catch (error) {
            alert("Lỗi rồi: Server đang bận đi chơi!");
        } finally {
            setIsLoading(false);
        }
    }
    if (cart.length === 0) {
        return (
            <div className="p-10 text-center">
                Giỏ hàng trống. <Link href="/" className="text-blue-500 underline">Đi mua sắm đi!</Link>
            </div>
        )
    }

    return (
        <div className="container mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* CỘT TRÁI: Form nhập liệu */}
            <div>
                <h2 className="text-2xl font-bold mb-6">Thông tin giao hàng</h2>
                <form onSubmit={handleOrder} className="space-y-4">
                    <div>
                        <label className="block text-gray-700 mb-1">Họ và tên</label>
                        <input
                            type="text"
                            name="fullName"
                            required
                            className="w-full border p-2 rounded focus:outline-none focus:border-blue-500"
                            placeholder="Ví dụ: Tiểu Muội Xinh Đẹp"
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-1">Số điện thoại</label>
                        <input
                            type="tel"
                            name="phone"
                            required
                            className="w-full border p-2 rounded focus:outline-none focus:border-blue-500"
                            placeholder="09xxx..."
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-1">Địa chỉ nhận hàng</label>
                        <textarea
                            name="address"
                            required
                            className="w-full border p-2 rounded focus:outline-none focus:border-blue-500 h-24"
                            placeholder="Số nhà, tên đường..."
                            onChange={handleChange}
                        ></textarea>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-3 text-white font-bold rounded-lg transition-colors ${isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
                    >
                        {isLoading ? 'Đang gửi đơn...' : `Thanh toán ${formatPrice(totalPrice)}`}
                    </button>
                </form>
            </div>

            {/* CỘT PHẢI: Tóm tắt đơn hàng */}
            <div className="bg-gray-50 p-6 rounded-xl border h-fit">
                <h3 className="text-xl font-bold mb-4">Đơn hàng của muội ({cart.length} món)</h3>
                <div className="space-y-3 max-h-80 overflow-y-auto pr-2">
                    {cart.map(item => (
                        <div key={item.id} className="flex justify-between items-center text-sm">
                            <span>{item.name} <span className="text-gray-500">x{item.quantity}</span></span>
                            <span className="font-medium">{formatPrice(item.price * item.quantity)}</span>
                        </div>
                    ))}
                </div>
                <div className="border-t mt-4 pt-4 flex justify-between font-bold text-lg">
                    <span>Tổng cộng:</span>
                    <span className="text-blue-600">{formatPrice(totalPrice)}</span>
                </div>
            </div>
        </div>
    );
}
export default CheckoutPage;