import { create } from "zustand";
import { Variant } from "@/app/types/Product";
import { CartItem } from "@/app/types/Cart";
import { persist, createJSONStorage } from 'zustand/middleware';


interface CartState {
    cart: CartItem[];
    totalItems: number;

    addToCart: (variant: Variant) => void;
    removeFromCart: (variantId: string) => void;
    decreaseQuantity: (variantId: string) => void;
    clearCart: () => void;

}

export const useCartStore = create<CartState>()(
    persist(
        (set) => ({
            cart: [],
            totalItems: 0,

            addToCart: (variant: Variant) => set((state) => {
                const existingItem = state.cart.find(item => item.id === variant.id);
                let newCart;

                if (existingItem) {
                    newCart = state.cart.map(item =>
                        item.id === variant.id
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    );
                } else {

                    newCart = [...state.cart, { ...variant, quantity: 1 }];
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

            decreaseQuantity: (variantId: string) => set((state) => {
                const newCart = state.cart.map(item => {
                    if (item.id === variantId) {
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
