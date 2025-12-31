import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'placehold.co', // Cho phép ông placehold.co vào nhà
        port: '',
        pathname: '/**', // Cho phép lấy mọi đường dẫn ảnh của nó
      },
    ],
  },
};

export default nextConfig;
