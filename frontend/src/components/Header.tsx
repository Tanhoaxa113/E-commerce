'use client'

import React, { useState } from 'react'
import { useCartStore } from '@/store/cartStore';
interface HeaderProps {
    shopName: string
}

const Header = ({ shopName }: HeaderProps) => {
    const [searchString, setSearchString] = useState<string>("")
    const totalItems = useCartStore((state) => state.totalItems);
    return (
        <header className='h-15 bg-blue-950 shadow-md flex items-center justify-between px-4 sticky top-0 z-50'>
            <div className='text-xl font-bold text-white cursor-pointer'>
                {shopName}
            </div>
            <div className='flex-1 mx-10 max-w-lg '>
                <input className='w-full border border-gray-50 rounded-full py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all'
                    type="text"
                    placeholder="Tìm kiếm sản phẩm"
                    value={searchString} onChange={(e) => setSearchString(e.target.value)}>
                </input>
            </div>
            <div className='flex items-center'>
                <button className="relative text-gray-600 hover:text-blue-500 transition-colors">
                    Giỏ hàng
                    {/* Hiển thị số lượng (Badge) */}
                    {totalItems > 0 && (
                        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full">
                            {totalItems}
                        </span>
                    )}
                </button>
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-semibold">
                    M
                </div>
            </div>
        </header>
    )
}
export default Header;