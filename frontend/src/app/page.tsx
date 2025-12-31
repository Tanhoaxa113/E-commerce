import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Trang chủ | TTG Shop',
  description: 'Đây là trang chủ',
}

export default function Home() {
  return (
    <div>
      <Link href="/login" className="btn-login">
        Đăng nhập
      </Link>
    </div>

  )
}