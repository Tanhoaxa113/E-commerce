export interface Image {
    id: string
    image: string
    alt_text: string
}
export interface Video {
    id: string
    thumbnail: string
    duration: any
    video_url: string
}
export interface Review {
    id: string
    user: string
    rating: number
    comment: string
    created_at: string
}
export interface Comment {
    id: string
    user: string
    comment: string
    created_at: string
}
export interface Variant {
    id: string
    sku: string
    price: string
    final_price: string
    discount_rate: number
    variant_specs: any

}
export interface Product {
    id: string
    name: string
    slug: string
    description: string
    variants: Variant[]
    images: Image[]
    videos: Video[]
    reviews: Review[]
    comments: Comment[]
}

export interface ProductCardProps {
    product: Product
}