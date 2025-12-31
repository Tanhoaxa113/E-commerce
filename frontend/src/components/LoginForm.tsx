export default function LoginForm() {
    return (
        <form>
            <label>
                Tên tài khoản
            
                <input type="text" />
            </label>
            <label>
                Mật khẩu
                <input type="password" />
            </label>
            <button type="submit">Đăng ký</button>
        </form>
    )
}