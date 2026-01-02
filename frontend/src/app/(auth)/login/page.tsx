'use client'

import React, { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"

const LoginPage = () => {
    const router = useRouter()
    const [step, setStep] = useState<1 | 2>(1)
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        otp: '',
    })
    const [tempUserId, setTempUserId] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState("")
    const [access, setAccess] = useState("")

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
        setError("")
    }
    const handleLoginStep1 = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)
        setError("")
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: formData.username,
                    password: formData.password
                }),
            })
            const response = await res.json()
            if (!res.ok) throw new Error(response.message || 'Sai tài khoản/mật khẩu!');
            if (response.required_otp) {
                setStep(2)
                setTempUserId(response.user_id)
            } else {
                finishLogin(response);
            }
        } catch (err: any) {
            setError(err.message || "Có lỗi xảy ra");
        } finally {
            setIsLoading(false);
        }
    }
    const handleVerifyOtp = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)
        setError("")
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/login/2fa/`, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: tempUserId,
                    otp: formData.otp,
                    username: formData.username,
                    password: formData.password
                }),
                
            })
            const response = await res.json()
            if (response.non_field_errors) throw new Error(response.non_field_errors)
            else finishLogin(response);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }
    const finishLogin = (response: any) => {
        localStorage.setItem('refreshToken', response.refresh_token);
        alert("Đăng nhập thành công mỹ mãn!");
        router.push('/');
    }
    return (
        <div className="w-full max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg border">
            <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">
                {step === 1 ? 'Đăng Nhập' : 'Xác Thực OTP'}
            </h2>

            {error && (
                <div className="mb-4 p-3 bg-red-100 text-red-600 rounded text-sm text-center">
                    {error}
                </div>
            )}

            {/* --- GIAO DIỆN BƯỚC 1: LOGIN --- */}
            {step === 1 && (
                <form onSubmit={handleLoginStep1} className="space-y-4">
                    <div>
                        <label className="block text-gray-700 mb-1">Username
                        <input
                            type="text" name="username"
                            value={formData.username} onChange={handleChange}
                            className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        </label>
                    </div>
                    <div>
                        <label className="block text-gray-700 mb-1">Mật khẩu
                        <input
                            type="password" name="password"
                            value={formData.password} onChange={handleChange}
                            className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        </label>
                    </div>
                    <button
                        type="submit" disabled={isLoading}
                        className="w-full py-2 bg-blue-600 text-white font-bold rounded hover:bg-blue-700 transition"
                    >
                        {isLoading ? 'Đang kiểm tra...' : 'Tiếp tục'}
                    </button>
                </form>
            )}

            {/* --- GIAO DIỆN BƯỚC 2: OTP --- */}
            {step === 2 && (
                <form onSubmit={handleVerifyOtp} className="space-y-4 animate-fade-in-up">
                    <div className="text-center text-sm text-gray-500 mb-4">
                        Chúng tôi đã gửi mã xác thực đến <b>{formData.username}</b>
                    </div>
                    <div>
                        <label className="block text-gray-700 mb-1">Nhập mã OTP</label>
                        <input
                            type="text" name="otp"
                            value={formData.otp} onChange={handleChange}
                            className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none text-center text-2xl tracking-widest font-mono"
                            placeholder="1A2B3C4D"
                            maxLength={8}
                            required
                        />
                    </div>
                    <button
                        type="submit" disabled={isLoading}
                        className="w-full py-2 bg-green-600 text-white font-bold rounded hover:bg-green-700 transition"
                    >
                        {isLoading ? 'Đang xác thực...' : 'Xác nhận OTP'}
                    </button>

                    <button
                        type="button"
                        onClick={() => setStep(1)} // Nút quay lại nếu nhập sai email
                        className="w-full text-gray-500 text-sm hover:underline mt-2"
                    >
                        Quay lại đăng nhập
                    </button>
                </form>
            )}
        </div>
    );
}
export default LoginPage;