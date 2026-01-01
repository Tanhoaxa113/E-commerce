'use client'

import React, { useState, useRef, useEffect, use} from 'react'
import { useCartStore } from '@/store/cartStore';
import Image from 'next/image';
import Link from 'next/link';
interface HeaderProps {
    shopName: string
}



const Header = ({ shopName }: HeaderProps) => {
    const [searchString, setSearchString] = useState<string>("")
    const totalItems = useCartStore((state) => state.totalItems);
    const { cart, removeFromCart } = useCartStore();
    const [isOpenCart, setIsOpenCart] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const buttonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
            function handleClickOutside(event: MouseEvent) {
                if (isOpenCart && dropdownRef.current && !dropdownRef.current.contains(event.target as Node)
                && buttonRef.current && !buttonRef.current.contains(event.target as Node)) {
                    setIsOpenCart(false);
                }}
                document.addEventListener("mousedown", handleClickOutside);

                return () => {
                    document.removeEventListener("mousedown", handleClickOutside);
                }
        })
    return (
        
        <header className='h-15 bg-blue-950 shadow-md flex items-center justify-between px-4 sticky top-0 z-50'>
            <div className='text-xl font-bold text-white cursor-pointer'>
                {shopName}
            </div>
            <div className='flex-1 mx-10 max-w-lg '>
                <input className='w-full border border-gray-50 rounded-full py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all text-white'
                    type="text"
                    placeholder="Tìm kiếm sản phẩm"
                    value={searchString} onChange={(e) => setSearchString(e.target.value)}>
                </input>
            </div>
            <div className='relative flex gap-4 items-center'>
                <button ref={buttonRef}
                    onClick={() => setIsOpenCart(!isOpenCart)}
                    className="text-gray-600 hover:text-blue-500 transition-colors py-2">
                    Giỏ hàng ({totalItems})
                </button>
                
                {isOpenCart && (
                    <div ref={dropdownRef} className="absolute right-0 top-full mt-2 w-80 bg-white shadow-xl rounded-lg border border-gray-100 p-4 z-50">
                        {cart.length === 0 ? (
                            <p className="text-center text-gray-500">Chưa có gì đâu bé ơi!</p>
                        ) : (
                            <div className="max-h-60 overflow-y-auto">
                                {cart.map((item) => (
                                    <div key={item.id} className="flex justify-between items-center mb-3 border-b pb-2">
                                        <div className="flex items-center gap-2">
                                            
                                            <div className="w-10 h-10 bg-gray-200 rounded">Img</div>
                                            <div>
                                                <p className="text-sm font-semibold truncate w-32">{item.name}</p>
                                                <p className="text-xs text-gray-500">{item.quantity} x {item.price}</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => removeFromCart(item.id)}
                                            className="text-red-400 hover:text-red-600 text-xs"
                                        >
                                            Xóa
                                        </button>
                                    </div>
                                ))}
                                <Link href="/cart" onClick={() => setIsOpenCart(!isOpenCart)} className="block text-center bg-blue-600 text-white py-2 rounded mt-2 hover:bg-blue-700">
                                    Xem giỏ hàng
                                </Link>
                            </div>
                        )}
                    </div>
                )}
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-semibold">
                    M
                </div>
            </div>
        </header>
    )
}
export default Header;