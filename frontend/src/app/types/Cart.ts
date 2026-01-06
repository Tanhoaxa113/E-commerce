import { Variant } from "@/app/types/Product";

export interface CartItem {
    id: string
    sku: string
    price: string
    final_price: string
    discount_rate: number
    variant_specs: any
}

export interface CartItem extends Variant{
    quantity: number
}