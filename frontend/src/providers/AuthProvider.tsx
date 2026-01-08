'use client';

import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import apiClient from '@/lib/axios';

export default function AuthProvider({ children }: { children: React.ReactNode }) {
    const setAuth = useAuthStore((state) => state.setAuth);
    const logout = useAuthStore((state) => state.logout);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await apiClient.get('/api/users/me/');
                setAuth(response.data);
            } catch (error) {
                logout();
            }
        };

        checkAuth();
    }, [setAuth, logout]);

    return <>{children}</>;
}