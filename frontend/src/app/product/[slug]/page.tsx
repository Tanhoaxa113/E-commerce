import { notFound } from "next/navigation";
import ProductDetailClient from "./ProductDetailClient";

async function getProduct(slug: string) {
    console.log("Server đang fetch slug:", slug);

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/products/${slug}/`, {
        cache: 'no-store',
    });

    if (!res.ok) {
        console.error("Lỗi fetch:", res.status);
        return null;
    }
    return res.json();
}

export default async function Page({ params }: { params: { slug: string } }) {
    const resolvedParams = await params;
    const { slug } = resolvedParams;

    const product = await getProduct(slug);

    if (!product) {
        return notFound();
    }

    return <ProductDetailClient product={product} />;
}