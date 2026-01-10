import { CartItem } from "./Cart"

export interface Address {
    province: string
    ward: string
    phone: string
    adress_line: string
}

export interface Order {
    id: string
    user: string
    items: CartItem[]
    total_amount: number
    shipping_address: Address
    created_at: string
    note?: string
}