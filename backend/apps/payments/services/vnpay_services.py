# payment/services.py
import hashlib
import hmac
import urllib.parse
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now

class VNPAYService:
    def __init__(self):
        # Lấy cấu hình từ settings (nhớ cài trong .env và settings.py nhé)
        self.vnp_TmnCode = settings.VNPAY_TMN_CODE
        self.vnp_HashSecret = settings.VNPAY_HASH_SECRET
        self.vnp_Url = settings.VNPAY_PAYMENT_URL
        self.vnp_ReturnUrl = settings.VNPAY_RETURN_URL

    def get_payment_url(self, txn_ref, amount, order_desc, ip_addr):
        """
        Hàm tạo URL thanh toán chuyển hướng sang VNPAY
        :param txn_ref: Mã giao dịch unique (VD: ORDER_123_123456)
        :param amount: Số tiền (VND) - kiểu Decimal hoặc int
        :param order_desc: Nội dung thanh toán
        :param ip_addr: IP của người dùng thực hiện thanh toán
        """
        
        # 1. Chuẩn bị dữ liệu input
        # Lưu ý: VNPAY yêu cầu số tiền phải nhân 100 (VD: 10,000 VND -> 1,000,000)
        # Ép kiểu int để bỏ phần thập phân
        vnp_Amount = int(amount * 100) 
        
        create_date = now().strftime('%Y%m%d%H%M%S') # Format: YYYYMMDDHHmmss
        
        # 2. Bộ tham số chuẩn của VNPAY
        inputData = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': self.vnp_TmnCode,
            'vnp_Amount': str(vnp_Amount),
            'vnp_CreateDate': create_date,
            'vnp_CurrCode': 'VND',
            'vnp_IpAddr': ip_addr,
            'vnp_Locale': 'vn',
            'vnp_OrderInfo': order_desc,
            'vnp_OrderType': 'other', # Có thể là 'billpayment', 'fashion'... tùy chọn
            'vnp_ReturnUrl': self.vnp_ReturnUrl,
            'vnp_TxnRef': txn_ref, # Mã tham chiếu độc nhất
        }

        # 3. Sắp xếp tham số theo bảng chữ cái (BẮT BUỘC)
        # Nếu không sort, checksum sẽ sai bét nhè.
        inputData = sorted(inputData.items())
        
        # 4. Tạo chuỗi query string
        # Kết quả dạng: key1=value1&key2=value2...
        qs = urllib.parse.urlencode(inputData)
        
        # 5. Tạo chữ ký bảo mật (Secure Hash)
        # VNPAY dùng thuật toán HMAC-SHA512
        if self.vnp_HashSecret:
            h = hmac.new(
                self.vnp_HashSecret.encode('utf-8'),
                qs.encode('utf-8'), 
                hashlib.sha512
            )
            vnp_SecureHash = h.hexdigest()
            
            # 6. Ghép chữ ký vào URL cuối cùng
            qs += '&vnp_SecureHash=' + vnp_SecureHash

        payment_url = self.vnp_Url + "?" + qs
        return payment_url

    def validate_signature(self, vnp_params):
        """
        Hàm kiểm tra chữ ký khi VNPAY gọi ngược lại (IPN hoặc Return URL)
        Để đảm bảo dữ liệu không bị giả mạo.
        """
        # Lấy secure hash từ params gửi về và loại bỏ nó khỏi dữ liệu cần hash
        vnp_SecureHash = vnp_params.get('vnp_SecureHash')
        
        # Copy và loại bỏ các tham số không tham gia tính hash
        data = vnp_params.copy()
        if 'vnp_SecureHash' in data:
            data.pop('vnp_SecureHash')
        if 'vnp_SecureHashType' in data:
            data.pop('vnp_SecureHashType')
            
        # Sắp xếp lại
        data = sorted(data.items())
        
        # Tạo lại chuỗi hash
        qs = urllib.parse.urlencode(data)
        h = hmac.new(
            self.vnp_HashSecret.encode('utf-8'),
            qs.encode('utf-8'), 
            hashlib.sha512
        )
        check_hash = h.hexdigest()
        
        # So sánh hash mình tính với hash VNPAY gửi
        return vnp_SecureHash == check_hash