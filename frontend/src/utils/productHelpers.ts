import { Variant } from "@/components/ProductCard";

export const getVariantPriceStats = (variants: Variant[]) => {
    if (!variants || variants.length === 0) {
        return{minFinalPrice: 0, maxOriginalPrice: 0};
    }

    const finalPrices = variants.map(v => Number(v.final_price))
    const originalPrices = variants.map(v => Number(v.price))

    const minFinalPrice = Math.min(...finalPrices)
    const maxOriginalPrice = Math.max(...originalPrices)

    return {
        minFinalPrice,
        maxOriginalPrice
    }
}