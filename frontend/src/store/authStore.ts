import { create} from 'zustand';
import { persist} from 'zustand/middleware';
import { CurrentUser } from '@/app/types/Auth';

interface AuthState {
    user: CurrentUser | null;
    isAuthenticated: boolean;

    setAuth: (apiData: any) => void;
    logout: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            isAuthenticated: false,

            setAuth: (data) => {
                const mappedUser: CurrentUser = {
                    id: data.id,
                    username: data.username,
                    email: data.email,
                    first_name: data.first_name,
                    last_name: data.last_name,
                    avatar: data.avatar,
                    gender: data.gender,
                    phone_number: data.phone_number,
                    address: data.address,
                    customer_type: data.customer_type,
                    loyalty_points: data.loyalty_points,
                    position: data.position,
                    work_address: data.work_address,
                    hire_date: data.hire_date,
                };
                set({ user: mappedUser, isAuthenticated: true });
            },
            logout: () => set({
                user: null,
                isAuthenticated: false
            }),
            
        }),
        { name: 'auth-storage' }
    )
);