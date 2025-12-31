import "./globals.css";
import type { Metadata } from 'next'
import Header from '@/components/Header';
import Footer from '@/components/Footer';

interface RootLayoutProps {
    children: React.ReactNode;
}

export const metadata: Metadata = {
    title: {
        template: '%s | TTG Shop',
        default: 'TTG Shop',
    },
    description: 'TTG Shop mua bán phụ kiện',
}
export default function Layout({ children }: RootLayoutProps) {
    return (
        <html>
            <body className="flex flex-col min-h-screen">
                <Header shopName="TTG Shop" />

                <main className="flex-1 container mx-auto p-4">
                    {children}
                </main>

                <Footer year= {new Date().getFullYear()} />
            </body>

        </html>
    )
}