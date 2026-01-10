import { Variant } from "@/app/types/Product";

export interface CartItem {
    id: string
    sku: string
    name: string
    price: number
    final_price: number
    discount_rate: number
    variant_specs: any
}

export interface CartItem extends Variant{
    quantity: number
}
