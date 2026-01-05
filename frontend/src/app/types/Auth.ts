export interface CurrentUser {
    id: string;
    username: string;
    email: string;
    
    first_name?: string;
    last_name?: string;
    avatar?: string;
    
    gender?: string;
    phone_number?: string;
    address?: string;
    customer_type?: 'BRONZE' | 'SILVER' | 'GOLD' | 'PLATINUM' | 'DIAMOND';
    loyalty_points?: number;

    position?: string;
    work_address?: string;
    hire_date?: string;
}