import { create } from "zustand";
import { Product } from "@/components/ProductCard";

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

}
export interface CartItem extends Product {
    quantity: number;
}

export const useCartStore = create<CartState>((set) => ({
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



}));
