import { create } from "zustand";
import { Product } from "@/components/ProductCard";
import { persist, createJSONStorage } from 'zustand/middleware';

export interface CartItem {
    id: string;
    name: string;
    price: number;
    image: string;
    quantity: number;
}

interface CartState {
    cart: CartItem[];
    totalItems: number;

    addToCart: (product: Product) => void;
    removeFromCart: (productId: string) => void;
    decreaseQuantity: (productId: string) => void;
    clearCart: () => void;

}
export interface CartItem extends Product {
    quantity: number;
}

export const useCartStore = create<CartState>()(
    persist(
        (set) => ({
            cart: [],
            totalItems: 0,

            addToCart: (product: Product) => set((state) => {
                const existingItem = state.cart.find(item => item.id === product.id);
                let newCart;

                if (existingItem) {
                    newCart = state.cart.map(item =>
                        item.id === product.id
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    );
                } else {

                    newCart = [...state.cart, { ...product, quantity: 1 }];
                }

                return {
                    cart: newCart,
                    totalItems: state.totalItems + 1
                };
            }),

            removeFromCart: (id) => set((state) => ({
                cart: state.cart.filter(item => item.id !== id),
                totalItems: state.totalItems - 1
            })),

            decreaseQuantity: (productId: string) => set((state) => {
                const newCart = state.cart.map(item => {
                    if (item.id === productId) {
                        // Logic chặn số âm: Nếu lớn hơn 1 mới cho trừ
                        if (item.quantity > 1) {
                            return { ...item, quantity: item.quantity - 1 };
                        }
                        // Nếu bằng 1 thì giữ nguyên (hoặc return null để xóa tùy muội)
                        return item;
                    }
                    return item;
                });

                return {
                    cart: newCart,
                    // Tính lại tổng số lượng icon trên Header
                    totalItems: newCart.reduce((acc, item) => acc + item.quantity, 0)
                };
            }),
            clearCart: () => set({ cart: [], totalItems: 0 }),
        }), {
            name: 'cart-storage', // name of the item in the storage (must be unique)
            storage: createJSONStorage(() => sessionStorage), // (optional) by default, 'localStorage' is used
        }
    )
);
