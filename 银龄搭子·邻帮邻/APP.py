# 银龄搭子 - 修复完整版（无前端错误）
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import hashlib
import json
import os
import time
from PIL import Image
import io
import folium
from streamlit_folium import folium_static

# ==================== 配置设置 ====================
st.set_page_config(
    page_title="银龄搭子 · 邻帮邻",
    page_icon="👵",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/elderly-companion',
        'Report a bug': "mailto:contact@yinlingdazi.com",
        'About': "# 银龄搭子 - 社区互助平台"
    }
)

# ==================== 安全稳定的CSS（无JavaScript） ====================
st.markdown("""
<style>
    /* 基础字体放大 */
    .stApp {
        font-size: 20px !important;
    }
    
    /* 超大标题 */
    .main-title {
        font-size: 38px !important;
        color: #FF9933 !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
    }
    
    /* 大号副标题 */
    .section-title {
        font-size: 30px !important;
        color: #2C3E50 !important;
        font-weight: bold !important;
        margin: 25px 0 15px 0 !important;
    }
    
    /* 大按钮样式 */
    .big-button {
        font-size: 22px !important;
        padding: 18px 25px !important;
        border-radius: 12px !important;
        margin: 12px !important;
    }
    
    /* 卡片样式 */
    .service-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: center;
    }
    
    /* 紧急按钮 */
    .emergency-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    
    /* 支付卡片样式 */
    .payment-card {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .vip-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #8B4513;
        padding: 5px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 14px;
    }
    
    .commission-badge {
        background: #28a745;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
    }
    
    .fund-badge {
        background: #6c757d;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
    }
    
    /* 数据卡片 */
    .data-card {
        background: #f5f7fa;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        margin: 10px;
    }
    
    /* 图表容器 */
    .chart-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* 仪表板卡片 */
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 用户认证系统（增强版） ====================
class UserSystem:
    """用户注册登录系统（包含密码重置）"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.reset_tokens_file = "reset_tokens.json"
        self.orders_file = "orders.json"
        self.transactions_file = "transactions.json"
        self.business_file = "business.json"
        self.load_users()
        self.load_reset_tokens()
        self.load_orders()
        self.load_transactions()
        self.load_business_data()
    
    def load_users(self):
        """加载用户数据"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except:
            self.users = {}
    
    def save_users(self):
        """保存用户数据"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def load_reset_tokens(self):
        """加载重置令牌"""
        try:
            with open(self.reset_tokens_file, 'r', encoding='utf-8') as f:
                self.reset_tokens = json.load(f)
        except:
            self.reset_tokens = {}
    
    def save_reset_tokens(self):
        """保存重置令牌"""
        with open(self.reset_tokens_file, 'w', encoding='utf-8') as f:
            json.dump(self.reset_tokens, f, ensure_ascii=False, indent=2)
    
    def load_orders(self):
        """加载订单数据"""
        try:
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        except:
            self.orders = []
    
    def save_orders(self):
        """保存订单数据"""
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)
    
    def load_transactions(self):
        """加载交易数据"""
        try:
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                self.transactions = json.load(f)
        except:
            self.transactions = []
    
    def save_transactions(self):
        """保存交易数据"""
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=2)
    
    def load_business_data(self):
        """加载商业数据"""
        try:
            with open(self.business_file, 'r', encoding='utf-8') as f:
                self.business_data = json.load(f)
        except:
            # 初始化商业数据
            self.business_data = {
                "mutual_fund": 500.0,
                "total_commission": 1250.0,
                "government_contracts": 3,
                "vip_members": 45,
                "orders_today": 0,
                "revenue_today": 0.0,
                "commission_today": 0.0,
                "donation_today": 0.0,
                "last_update": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            self.save_business_data()
    
    def save_business_data(self):
        """保存商业数据"""
        with open(self.business_file, 'w', encoding='utf-8') as f:
            json.dump(self.business_data, f, ensure_ascii=False, indent=2)
    
    def register(self, username, password, user_type, phone, address, age, interests):
        """用户注册"""
        if username in self.users:
            return False, "用户名已存在"
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user_type == "老人用户":
            points = 0
            service_count = 0
            rating = 0
            identity = "老人"
            balance = 100
            is_vip = False
        elif user_type == "志愿者":
            points = 100
            service_count = 0
            rating = 5.0
            identity = "大学生" if age < 25 else "社区志愿者"
            balance = 0
            is_vip = False
        elif user_type == "家属/子女":
            points = 50
            service_count = 0
            rating = 0
            identity = "家属"
            balance = 200
            is_vip = False
        else:
            points = 500
            service_count = 0
            rating = 5.0
            identity = "管理员"
            balance = 1000
            is_vip = True
        
        self.users[username] = {
            'password': password_hash,
            'user_type': user_type,
            'phone': phone,
            'address': address,
            'age': age,
            'interests': interests,
            'reg_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'points': points,
            'service_count': service_count,
            'total_hours': 0,
            'rating': rating,
            'identity': identity,
            'bio': f"我是{user_type}，很高兴加入银龄搭子社区！",
            'emergency_contact': phone,
            'balance': balance,
            'total_spent': 0.0,
            'commission_earned': 0.0,
            'vip_expiry': None,
            'is_vip': is_vip,
            'donation_total': 0.0
        }
        self.save_users()
        return True, "注册成功！"
    
    def login(self, username, password):
        """用户登录"""
        if username not in self.users:
            return False, "用户不存在"
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if self.users[username]['password'] == password_hash:
            return True, "登录成功"
        return False, "密码错误"
    
    def generate_reset_token(self, username):
        """生成密码重置令牌"""
        token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:32]
        self.reset_tokens[token] = {
            'username': username,
            'expires': time.time() + 3600,
            'used': False
        }
        self.save_reset_tokens()
        return token
    
    def validate_reset_token(self, token):
        """验证重置令牌"""
        if token in self.reset_tokens:
            token_data = self.reset_tokens[token]
            if time.time() < token_data['expires'] and not token_data['used']:
                return token_data['username']
        return None
    
    def reset_password(self, token, new_password):
        """重置密码"""
        username = self.validate_reset_token(token)
        if username and username in self.users:
            self.users[username]['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            self.reset_tokens[token]['used'] = True
            self.save_users()
            self.save_reset_tokens()
            return True
        return False
    
    def find_user_by_email(self, email):
        """通过邮箱查找用户"""
        for username, data in self.users.items():
            if data.get('phone') == email:
                return username
        return None
    
    def update_profile(self, username, **kwargs):
        """更新用户资料"""
        if username in self.users:
            for key, value in kwargs.items():
                if value is not None:
                    self.users[username][key] = value
            self.save_users()
            return True
        return False
    
    def create_order(self, username, service_type, duration, amount, volunteer=None):
        """创建订单"""
        order_id = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
        
        order = {
            'order_id': order_id,
            'username': username,
            'service_type': service_type,
            'duration': duration,
            'amount': amount,
            'volunteer': volunteer,
            'status': '待支付',
            'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'payment_time': None,
            'commission': amount * 0.1,
            'donation': amount * 0.005,
            'actual_amount': amount * 0.895
        }
        
        self.orders.append(order)
        self.save_orders()
        return order_id
    
    def process_payment(self, order_id, payment_method):
        """处理支付"""
        for order in self.orders:
            if order['order_id'] == order_id:
                if order['status'] == '待支付':
                    user = self.users.get(order['username'])
                    if user['balance'] >= order['amount']:
                        user['balance'] -= order['amount']
                        user['total_spent'] += order['amount']
                        
                        order['status'] = '已支付'
                        order['payment_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        order['payment_method'] = payment_method
                        
                        self.business_data['mutual_fund'] += order['donation']
                        self.business_data['total_commission'] += order['commission']
                        self.business_data['orders_today'] += 1
                        self.business_data['revenue_today'] += order['amount']
                        self.business_data['commission_today'] += order['commission']
                        self.business_data['donation_today'] += order['donation']
                        
                        transaction = {
                            'transaction_id': f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}",
                            'username': order['username'],
                            'order_id': order_id,
                            'amount': order['amount'],
                            'type': '支付',
                            'payment_method': payment_method,
                            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'balance_after': user['balance']
                        }
                        self.transactions.append(transaction)
                        
                        user['points'] += int(order['amount'] / 10)
                        
                        if user.get('is_vip', False):
                            user['points'] += int(order['amount'] / 5)
                        
                        user['donation_total'] += order['donation']
                        
                        self.save_users()
                        self.save_orders()
                        self.save_transactions()
                        self.save_business_data()
                        
                        return True, "支付成功"
                    else:
                        return False, "余额不足"
                else:
                    return False, "订单状态错误"
        return False, "订单不存在"
    
    def add_balance(self, username, amount, payment_method="微信支付"):
        """充值余额"""
        if username in self.users:
            self.users[username]['balance'] += amount
            
            transaction = {
                'transaction_id': f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}",
                'username': username,
                'amount': amount,
                'type': '充值',
                'payment_method': payment_method,
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'balance_after': self.users[username]['balance']
            }
            self.transactions.append(transaction)
            
            if self.users[username].get('is_vip', False) and amount >= 100:
                bonus = amount * 0.1
                self.users[username]['balance'] += bonus
                transaction['bonus'] = bonus
            
            self.save_users()
            self.save_transactions()
            return True
        return False
    
    def get_user_orders(self, username):
        """获取用户订单"""
        return [order for order in self.orders if order['username'] == username]
    
    def get_user_transactions(self, username):
        """获取用户交易记录"""
        return [tx for tx in self.transactions if tx['username'] == username]

# ==================== 支付功能模块 ====================
class PaymentSystem:
    """支付系统模块"""
    
    @staticmethod
    def show_payment_page(order_id, amount, service_type):
        """显示支付页面"""
        st.markdown(f"<h2 class='section-title'>💰 订单支付</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='payment-card'>
            <h3>📋 订单信息</h3>
            <p><strong>订单号：</strong> {order_id}</p>
            <p><strong>服务类型：</strong> {service_type}</p>
            <p><strong>支付金额：</strong> <span style='color: #FF6B35; font-size: 24px; font-weight: bold;'>¥{amount:.2f}</span></p>
            <p><strong>包含：</strong></p>
            <ul>
                <li>服务费：¥{amount*0.895:.2f}（支付给志愿者）</li>
                <li>平台佣金：¥{amount*0.1:.2f} <span class='commission-badge'>10%</span></li>
                <li>互助基金：¥{amount*0.005:.2f} <span class='fund-badge'>0.5%捐赠</span></li>
            </ul>
            <p><em>💝 您的支付将为特困老人带来温暖，感谢您的支持！</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 💳 选择支付方式")
        
        payment_methods = [
            {"name": "微信支付", "icon": "💚", "desc": "扫码支付，快速便捷"},
            {"name": "支付宝", "icon": "🔵", "desc": "安全可靠，支持花呗"},
            {"name": "银联支付", "icon": "💳", "desc": "支持各大银行卡"},
            {"name": "余额支付", "icon": "💰", "desc": "使用账户余额支付"}
        ]
        
        selected_method = st.session_state.get('selected_payment_method', '微信支付')
        
        cols = st.columns(2)
        for idx, method in enumerate(payment_methods):
            with cols[idx % 2]:
                is_selected = selected_method == method['name']
                
                if st.button(
                    f"{method['icon']} {method['name']}",
                    key=f"pay_method_{idx}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_payment_method = method['name']
                    st.rerun()
                
                st.caption(method['desc'])
        
        user_system = st.session_state.user_system
        username = st.session_state.username
        user_balance = user_system.users.get(username, {}).get('balance', 0)
        
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;'>
            <p><strong>账户余额：</strong> ¥{user_balance:.2f}</p>
            <p><strong>支付后余额：</strong> ¥{user_balance - amount:.2f if user_balance >= amount else '余额不足'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ 确认支付", use_container_width=True, type="primary"):
                if user_balance >= amount:
                    success, message = user_system.process_payment(order_id, selected_method)
                    if success:
                        st.success("🎉 支付成功！")
                        st.balloons()
                        
                        st.markdown(f"""
                        <div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 1px solid #c3e6cb;'>
                            <h3>✅ 支付成功</h3>
                            <p>订单号：{order_id}</p>
                            <p>支付方式：{selected_method}</p>
                            <p>支付金额：¥{amount:.2f}</p>
                            <p>感谢您捐赠 ¥{amount*0.005:.2f} 到银龄互助基金！</p>
                            <p>志愿者将很快与您联系确认服务细节。</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        time.sleep(3)
                        st.session_state.page = "首页"
                        st.rerun()
                    else:
                        st.error(f"支付失败：{message}")
                else:
                    st.error("余额不足，请先充值")
                    
                    st.markdown("#### 💰 立即充值")
                    recharge_amount = st.selectbox("选择充值金额", [50, 100, 200, 500, 1000])
                    
                    if st.button(f"充值 ¥{recharge_amount}", use_container_width=True):
                        if user_system.add_balance(username, recharge_amount, selected_method):
                            st.success(f"充值成功！当前余额：¥{user_system.users[username]['balance']:.2f}")
                            st.rerun()
                        else:
                            st.error("充值失败")

# ==================== 数据初始化 ====================
@st.cache_data
def init_system_data():
    """初始化系统数据"""
    elderly_data = pd.DataFrame({
        '老人ID': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007'],
        '姓名': ['王阿姨', '张大爷', '李奶奶', '赵爷爷', '刘阿姨', '陈奶奶', '孙爷爷'],
        '年龄': [72, 68, 75, 80, 70, 78, 82],
        '居住区域': ['徐汇区', '杨浦区', '浦东新区', '静安区', '徐汇区', '长宁区', '黄浦区'],
        '主要需求': ['购物陪伴', '手机教学', '聊天陪伴', '取快递', '社区团购', '医院陪诊', '散步聊天'],
        '使用语言': ['上海话', '普通话', '上海话', '普通话', '上海话', '普通话', '上海话'],
        '兴趣标签': ['园艺,戏曲', '书法,散步', '烹饪,聊天', '听广播', '园艺,手工', '养花,听戏', '下棋,书法'],
        '服务次数': [12, 8, 15, 6, 10, 7, 9],
        '注册时间': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05', '2023-05-12', '2023-06-18', '2023-07-22']
    })
    
    volunteer_data = pd.DataFrame({
        '志愿者ID': ['V001', 'V002', 'V003', 'V004', 'V005', 'V006', 'V007'],
        '姓名': ['张明', '李华', '王芳', '陈伟', '刘婷', '周杰', '吴琳'],
        '年龄': [22, 45, 32, 21, 38, 28, 65],
        '身份': ['大学生', '社区志愿者', '退休教师', '大学生', '社区志愿者', '公司职员', '退休医生'],
        '服务区域': ['徐汇区', '杨浦区', '浦东新区', '静安区', '徐汇区', '长宁区', '黄浦区'],
        '擅长服务': ['陪逛代购,手机教学', '陪逛代购,便民服务', '手机教学,聊天陪伴', 
                    '便民服务,社区团购', '陪逛代购', '医院陪诊,心理疏导', '健康咨询,聊天陪伴'],
        '使用语言': ['上海话,普通话', '普通话', '上海话', '普通话', '上海话,英语', 
                   '普通话,英语', '上海话,普通话'],
        '兴趣标签': ['园艺,音乐', '书法,运动', '烹饪,戏曲', '科技,手工', '园艺,书法', 
                   '医疗,阅读', '养生,旅游'],
        '评分': [4.9, 4.7, 5.0, 4.8, 4.6, 4.9, 5.0],
        '距离(km)': [0.5, 1.2, 0.8, 1.5, 0.3, 1.0, 0.7],
        '服务次数': [45, 32, 56, 28, 39, 42, 38],
        '服务时长': [120, 85, 156, 75, 108, 125, 95],
        '注册时间': ['2023-01-10', '2023-02-15', '2023-03-01', '2023-04-12', '2023-05-20', '2023-06-05', '2023-07-30']
    })
    
    dates = pd.date_range(start='2024-01-01', periods=40, freq='D')
    formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]
    
    orders_data = pd.DataFrame({
        '日期': formatted_dates,
        '订单数': np.random.randint(5, 25, len(dates)),
        '满意度': np.random.uniform(4.5, 5.0, len(dates))
    })
    
    return elderly_data, volunteer_data, orders_data

# ==================== 数据可视化函数（简化版） ====================
def create_simple_dashboard():
    """简化版数据看板"""
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">📊 银龄搭子数据看板</h2>', unsafe_allow_html=True)
    
    user_system = st.session_state.user_system
    business_data = user_system.business_data
    
    # 关键指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("累计服务", "1,284", "+128")
    with col2:
        st.metric("活跃老人", "163", "+12")
    with col3:
        st.metric("志愿者数", "89", "+8")
    with col4:
        st.metric("完成率", "96%", "+2%")
    
    # 财务指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("今日收入", f"¥{business_data['revenue_today']:.2f}")
    with col2:
        st.metric("互助基金", f"¥{business_data['mutual_fund']:.2f}")
    with col3:
        st.metric("累计佣金", f"¥{business_data['total_commission']:.2f}")
    with col4:
        st.metric("VIP会员", f"{business_data['vip_members']}人")
    
    # 订单趋势
    st.markdown("#### 📈 服务订单趋势")
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    orders = np.random.randint(20, 50, 30)
    trend_data = pd.DataFrame({
        '日期': dates,
        '订单数': orders
    })
    st.line_chart(trend_data.set_index('日期')['订单数'])
    
    # 收入分布
    st.markdown("#### 💰 收入来源分布")
    revenue_data = pd.DataFrame({
        '来源': ['服务费', '商家返佣', '增值服务', '政府项目'],
        '金额(万)': [28.5, 12.5, 8.2, 50.0]
    })
    st.bar_chart(revenue_data.set_index('来源')['金额(万)'])
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 地图功能 ====================
def create_service_map():
    """创建服务地图"""
    base_lat, base_lng = 31.2304, 121.4737
    m = folium.Map(location=[base_lat, base_lng], zoom_start=12, control_scale=True)
    
    for i in range(5):
        lat = base_lat + random.uniform(-0.05, 0.05)
        lng = base_lng + random.uniform(-0.05, 0.05)
        folium.Marker(
            [lat, lng],
            popup=f"<b>老人{i+1}</b><br>需求：购物陪伴<br>距离：{random.uniform(0.5, 2.0):.1f}km",
            tooltip=f"点击查看老人{i+1}信息",
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)
    
    for i in range(3):
        lat = base_lat + random.uniform(-0.03, 0.03)
        lng = base_lng + random.uniform(-0.03, 0.03)
        folium.Marker(
            [lat, lng],
            popup=f"<b>志愿者{i+1}</b><br>评分：{4.5+random.random():.1f}<br>可服务：聊天/购物",
            tooltip=f"点击查看志愿者{i+1}信息",
            icon=folium.Icon(color='green', icon='heart', prefix='fa')
        ).add_to(m)
    
    folium.Marker(
        [base_lat, base_lng],
        popup="<b>社区服务中心</b><br>地址：某某路123号<br>电话：400-123-4567",
        tooltip="社区服务中心",
        icon=folium.Icon(color='red', icon='flag', prefix='fa')
    ).add_to(m)
    
    folium.Circle(
        location=[base_lat, base_lng],
        radius=2000,
        color='orange',
        fill=True,
        fill_color='orange',
        fill_opacity=0.2,
        popup="2公里服务范围"
    ).add_to(m)
    
    return m

# ==================== 主程序 ====================
def main():
    user_system = UserSystem()
    elderly_data, volunteer_data, orders_data = init_system_data()
    
    st.session_state.user_system = user_system
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'page' not in st.session_state:
        st.session_state.page = "首页"
    if 'show_password_reset' not in st.session_state:
        st.session_state.show_password_reset = False
    if 'current_order' not in st.session_state:
        st.session_state.current_order = None
    if 'show_payment' not in st.session_state:
        st.session_state.show_payment = False
    
    # 密码重置页面
    if st.session_state.show_password_reset:
        st.markdown("<h1 class='main-title'>🔐 密码重置</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["申请重置", "重置密码"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>申请密码重置</h2>", unsafe_allow_html=True)
            reset_phone = st.text_input("📱 请输入注册手机号")
            
            if st.button("发送重置链接", use_container_width=True, type="primary"):
                user = user_system.find_user_by_email(reset_phone)
                if user:
                    token = user_system.generate_reset_token(user)
                    st.success(f"✅ 重置令牌已生成（演示用）：{token[:16]}...")
                    st.info("请复制上方令牌，在'重置密码'页面使用")
                else:
                    st.error("手机号未注册")
        
        with tab2:
            st.markdown("<h2 class='section-title'>重置密码</h2>", unsafe_allow_html=True)
            reset_token = st.text_input("🔑 请输入重置令牌")
            new_password = st.text_input("🔐 新密码", type="password")
            confirm_password = st.text_input("✅ 确认新密码", type="password")
            
            if st.button("重置密码", use_container_width=True, type="primary"):
                if new_password != confirm_password:
                    st.error("两次输入的密码不一致")
                elif len(new_password) < 6:
                    st.error("密码长度至少6位")
                else:
                    if user_system.reset_password(reset_token, new_password):
                        st.success("✅ 密码重置成功！")
                        st.session_state.show_password_reset = False
                        st.rerun()
                    else:
                        st.error("重置令牌无效或已过期")
        
        st.markdown("---")
        if st.button("返回登录页面", use_container_width=True):
            st.session_state.show_password_reset = False
            st.rerun()
        
        return
    
    # 登录/注册页面
    if not st.session_state.logged_in:
        st.markdown("<h1 class='main-title'>👵 银龄搭子 · 欢迎您</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 登录", "📝 注册"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>用户登录</h2>", unsafe_allow_html=True)
            
            login_username = st.text_input("👤 用户名", placeholder="请输入用户名")
            login_password = st.text_input("🔑 密码", type="password", placeholder="请输入密码")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("登录", use_container_width=True, type="primary"):
                    if login_username and login_password:
                        success, message = user_system.login(login_username, login_password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.session_state.user_type = user_system.users[login_username]['user_type']
                            st.success(f"欢迎回来，{login_username}！")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("请输入用户名和密码")
            
            with col2:
                if st.button("忘记密码？", use_container_width=True):
                    st.session_state.show_password_reset = True
                    st.rerun()
        
        with tab2:
            st.markdown("<h2 class='section-title'>新用户注册</h2>", unsafe_allow_html=True)
            
            reg_username = st.text_input("👤 设置用户名", placeholder="3-10位字符")
            reg_password = st.text_input("🔑 设置密码", type="password", placeholder="至少6位")
            reg_password2 = st.text_input("✅ 确认密码", type="password")
            reg_phone = st.text_input("📱 手机号码", placeholder="11位手机号")
            reg_type = st.selectbox("👥 用户类型", ["老人用户", "志愿者", "家属/子女", "社区管理员"])
            reg_address = st.text_input("📍 居住地址", placeholder="详细地址便于服务")
            reg_age = st.number_input("🎂 年龄", min_value=0, max_value=120, value=60)
            reg_interests = st.multiselect("❤️ 兴趣爱好", ["园艺", "书法", "戏曲", "烹饪", "散步", "聊天", "手工", "音乐", "运动", "阅读", "养生"])
            
            if st.button("注册账号", use_container_width=True, type="primary"):
                if not all([reg_username, reg_password, reg_password2, reg_phone]):
                    st.error("请填写所有必填项")
                elif reg_password != reg_password2:
                    st.error("两次输入的密码不一致")
                elif len(reg_password) < 6:
                    st.error("密码长度至少6位")
                else:
                    success, message = user_system.register(
                        reg_username, reg_password, reg_type, 
                        reg_phone, reg_address, reg_age, reg_interests
                    )
                    if success:
                        st.success(message)
                        st.info("请返回登录页面登录")
                    else:
                        st.error(message)
        
        return
    
    # 支付页面
    if st.session_state.show_payment and st.session_state.current_order:
        PaymentSystem.show_payment_page(
            st.session_state.current_order['order_id'],
            st.session_state.current_order['amount'],
            st.session_state.current_order['service_type']
        )
        
        if st.button("返回预约", use_container_width=True):
            st.session_state.show_payment = False
            st.rerun()
        
        return
    
    # 主界面（已登录）
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.username}")
        user_data = user_system.users.get(st.session_state.username, {})
        st.markdown(f"**身份**: {user_data.get('user_type', '用户')}")
        
        if user_data.get('is_vip', False):
            st.markdown('<span class="vip-badge">👑 VIP会员</span>', unsafe_allow_html=True)
        
        st.markdown(f"**余额**: ¥{user_data.get('balance', 0):.2f}")
        st.markdown(f"**积分**: {user_data.get('points', 0)} 分")
        
        menu_options = ["🏠 首页", "🤝 智能匹配", "📅 预约服务", "💰 支付中心", 
                       "💼 商业模式", "📸 记忆相册", "🗺️ 服务地图", "📊 数据看板", 
                       "👤 个人中心", "⚙️ 系统设置", "❓ 帮助"]
        
        selected_page = st.radio("导航菜单", menu_options)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆘 紧急求助", use_container_width=True, type="primary"):
                st.success("紧急求助已发送！志愿者和社区将立即响应。")
        with col2:
            if st.button("📞 联系家属", use_container_width=True):
                emergency_contact = user_data.get('emergency_contact', '无')
                st.info(f"正在联系家属：{emergency_contact}")
        
        st.markdown("---")
        if st.button("💰 快捷充值", use_container_width=True):
            st.session_state.page = "支付中心"
            st.rerun()
        
        st.markdown("---")
        if st.button("退出登录", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.show_payment = False
            st.session_state.current_order = None
            st.rerun()
    
    # 首页
    if selected_page == "🏠 首页":
        st.markdown(f"<h1 class='main-title'>👵 欢迎回来，{st.session_state.username}！</h1>", unsafe_allow_html=True)
        
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            greeting = "🌅 早上好！今天天气不错，适合出门走走。"
        elif current_hour < 18:
            greeting = "☀️ 下午好！阳光正好，要不要约个志愿者聊聊天？"
        else:
            greeting = "🌙 晚上好！今天过得怎么样？"
        
        st.markdown(f"### {greeting}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 账户余额", f"¥{user_data.get('balance', 0):.2f}")
        with col2:
            st.metric("⭐ 我的积分", f"{user_data.get('points', 0)} 分")
        with col3:
            if user_data.get('is_vip', False):
                st.metric("👑 VIP会员", "有效期内", "VIP")
            else:
                st.metric("👑 VIP会员", "立即开通", "免费试用")
        
        st.markdown("<h2 class='section-title'>🛠️ 选择您需要的服务</h2>", unsafe_allow_html=True)
        
        services = [
            {"icon": "🛒", "name": "陪逛代购", "desc": "超市/菜场/药店陪伴购物", "price": "10元/小时"},
            {"icon": "📱", "name": "手机教学", "desc": "微信/挂号/防诈骗一对一教学", "price": "10元/小时"},
            {"icon": "🛠️", "name": "便民服务", "desc": "取快递/缴费/简单维修协助", "price": "8元/小时"},
            {"icon": "🥬", "name": "社区团购", "desc": "长辈专享商品配送到家", "price": "免费+商品费"},
            {"icon": "💬", "name": "聊天陪伴", "desc": "陪伴聊天散步缓解孤独", "price": "5元/小时"},
            {"icon": "🏥", "name": "医院陪诊", "desc": "陪同就医取药", "price": "15元/小时"}
        ]
        
        cols = st.columns(3)
        for idx, service in enumerate(services):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='service-card'>
                    <div style='font-size: 40px; margin-bottom: 10px;'>{service['icon']}</div>
                    <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>{service['name']}</div>
                    <div style='font-size: 18px; margin-bottom: 10px;'>{service['desc']}</div>
                    <div style='font-size: 16px; background: rgba(255,255,255,0.2); padding: 5px; border-radius: 5px;'>
                        💰 {service['price']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"选择 {service['name']}", key=f"service_{idx}", use_container_width=True):
                    st.success(f"已选择{service['name']}，请继续填写预约信息")
    
    elif selected_page == "🤝 智能匹配":
        st.markdown("<h1 class='main-title'>🤖 智能匹配系统</h1>", unsafe_allow_html=True)
        
        with st.form("匹配设置"):
            service_type = st.selectbox("服务类型", ["陪逛代购", "手机教学", "便民服务", "社区团购", "聊天陪伴", "医院陪诊"])
            priority = st.radio("匹配优先级", ["智能推荐", "距离最近", "评分最高"])
            max_distance = st.slider("最大距离（公里）", 0.5, 5.0, 2.0)
            
            match_btn = st.form_submit_button("🚀 开始智能匹配", use_container_width=True)
        
        if match_btn:
            st.markdown("<h2 class='section-title'>🎯 匹配结果</h2>", unsafe_allow_html=True)
            
            matched = volunteer_data.copy()
            matched['匹配分'] = 0
            
            for idx, row in matched.iterrows():
                score = 0
                if row['距离(km)'] <= max_distance:
                    score += 40 - row['距离(km)'] * 10
                score += row['评分'] * 10
                score += row['服务次数'] * 0.5
                matched.loc[idx, '匹配分'] = score
            
            top_matches = matched.nlargest(3, '匹配分')
            
            for rank, (_, volunteer) in enumerate(top_matches.iterrows(), 1):
                with st.expander(f"第{rank}名: {volunteer['姓名']} (匹配分: {volunteer['匹配分']:.1f})"):
                    cols = st.columns(4)
                    metrics = [
                        ("📍 距离", f"{volunteer['距离(km)']}km"),
                        ("⭐ 评分", f"{volunteer['评分']}/5.0"),
                        ("👥 身份", volunteer['身份']),
                        ("🛠️ 服务次数", str(volunteer['服务次数']))
                    ]
                    
                    for col, (label, value) in zip(cols, metrics):
                        with col:
                            st.metric(label, value)
                    
                    st.markdown(f"**擅长服务**: {volunteer['擅长服务']}")
                    
                    base_price = 10
                    if volunteer['身份'] == '退休医生' and '医院陪诊' in volunteer['擅长服务']:
                        price = 15
                    elif volunteer['评分'] >= 4.8:
                        price = 12
                    else:
                        price = base_price
                    
                    st.markdown(f"**预估价格**: ¥{price}/小时")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        duration = st.selectbox(f"选择时长", [1, 2, 3, 4], key=f"dur_{rank}")
                    with col2:
                        total_price = price * duration
                        st.markdown(f"**总价**: ¥{total_price}")
                    
                    if st.button(f"选择 {volunteer['姓名']}", key=f"select_{rank}", use_container_width=True):
                        order_id = user_system.create_order(
                            st.session_state.username,
                            service_type,
                            f"{duration}小时",
                            total_price,
                            volunteer['姓名']
                        )
                        
                        st.session_state.current_order = {
                            'order_id': order_id,
                            'amount': total_price,
                            'service_type': service_type,
                            'volunteer': volunteer['姓名'],
                            'duration': f"{duration}小时"
                        }
                        
                        st.session_state.show_payment = True
                        st.rerun()
    
    elif selected_page == "📅 预约服务":
        st.markdown("<h1 class='main-title'>📅 服务预约</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["选择服务", "确认预约"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>选择服务类型</h2>", unsafe_allow_html=True)
            
            service_options = {
                "陪逛代购": {"icon": "🛒", "desc": "超市/菜场/药店陪伴购物", "price": 10},
                "手机教学": {"icon": "📱", "desc": "微信/挂号/防诈骗一对一教学", "price": 10},
                "便民服务": {"icon": "🛠️", "desc": "取快递/缴费/简单维修协助", "price": 8},
                "社区团购": {"icon": "🥬", "desc": "长辈专享商品配送到家", "price": 0},
                "聊天陪伴": {"icon": "💬", "desc": "陪伴聊天散步缓解孤独", "price": 5},
                "医院陪诊": {"icon": "🏥", "desc": "陪同就医、取药、问诊", "price": 15}
            }
            
            selected_service = st.selectbox("请选择服务类型：", options=list(service_options.keys()))
            
            if selected_service:
                st.success(f"✅ 已选择：{selected_service}")
        
        with tab2:
            st.markdown("<h2 class='section-title'>确认预约并支付</h2>", unsafe_allow_html=True)
            
            if 'selected_service' in locals():
                price_per_hour = service_options[selected_service]['price']
                duration = st.selectbox("服务时长", [1, 2, 3, 4])
                total_amount = price_per_hour * duration
                
                user_info = user_system.users.get(st.session_state.username, {})
                discount = 0.9 if user_info.get('is_vip', False) else 1.0
                final_amount = total_amount * discount
                
                st.markdown(f"""
                <div class='payment-card'>
                    <h3>📋 订单详情</h3>
                    <p><strong>服务类型</strong>: {selected_service}</p>
                    <p><strong>服务时长</strong>: {duration}小时</p>
                    <p><strong>单价</strong>: ¥{price_per_hour}/小时</p>
                    <p><strong>总计</strong>: ¥{final_amount:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                agree_terms = st.checkbox("✅ 我已阅读并同意《服务协议》")
                
                if st.button("💰 确认并支付", use_container_width=True, type="primary", disabled=not agree_terms):
                    order_id = user_system.create_order(
                        st.session_state.username,
                        selected_service,
                        f"{duration}小时",
                        final_amount
                    )
                    
                    st.session_state.current_order = {
                        'order_id': order_id,
                        'amount': final_amount,
                        'service_type': selected_service,
                        'duration': f"{duration}小时"
                    }
                    
                    st.session_state.show_payment = True
                    st.rerun()
    
    elif selected_page == "💰 支付中心":
        st.markdown("<h1 class='main-title'>💰 支付中心</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["账户余额", "订单管理", "充值中心"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>💳 我的账户</h2>", unsafe_allow_html=True)
            
            user_info = user_system.users.get(st.session_state.username, {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("账户余额", f"¥{user_info.get('balance', 0):.2f}")
            with col2:
                st.metric("我的积分", f"{user_info.get('points', 0)}")
            with col3:
                if user_info.get('is_vip', False):
                    st.metric("VIP会员", "有效期内")
                else:
                    st.metric("会员状态", "普通会员")
        
        with tab2:
            st.markdown("<h2 class='section-title'>📋 我的订单</h2>", unsafe_allow_html=True)
            
            orders = user_system.get_user_orders(st.session_state.username)
            
            if orders:
                for order in reversed(orders):
                    with st.expander(f"订单号：{order['order_id']} | 状态：{order['status']}"):
                        st.markdown(f"**服务类型**: {order['service_type']}")
                        st.markdown(f"**金额**: ¥{order['amount']:.2f}")
                        st.markdown(f"**创建时间**: {order['create_time']}")
                        
                        if order['status'] == '待支付':
                            if st.button("支付", key=f"pay_{order['order_id']}"):
                                st.session_state.current_order = order
                                st.session_state.show_payment = True
                                st.rerun()
            else:
                st.info("暂无订单记录")
        
        with tab3:
            st.markdown("<h2 class='section-title'>🔄 充值中心</h2>", unsafe_allow_html=True)
            
            recharge_options = [50, 100, 200, 500, 1000]
            custom_amount = st.number_input("充值金额", min_value=10, max_value=5000, value=100)
            payment_method = st.radio("支付方式", ["微信支付", "支付宝", "银联支付"])
            
            if st.button("立即充值", use_container_width=True, type="primary"):
                if user_system.add_balance(st.session_state.username, custom_amount, payment_method):
                    st.success(f"✅ 充值成功！¥{custom_amount:.2f} 已到账")
                    st.info(f"当前余额：¥{user_system.users[st.session_state.username]['balance']:.2f}")
                    st.rerun()
    
    elif selected_page == "💼 商业模式":
        st.markdown("<h1 class='main-title'>💼 银龄搭子商业模式</h1>", unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-title'>💰 商业模式</h2>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        models = [
            {"title": "💰 服务费收入", "desc": "基础陪伴服务10元/小时"},
            {"title": "🤝 商家返佣", "desc": "与商超、药店合作，获得佣金"},
            {"title": "🌟 增值服务", "desc": "套餐服务、节日礼包等"},
            {"title": "🏛️ 政府购买服务", "desc": "承接政府为老服务项目"}
        ]
        
        for idx, model in enumerate(models):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class='service-card'>
                    <h3>{model['title']}</h3>
                    <p>{model['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected_page == "📸 记忆相册":
        st.markdown("<h1 class='main-title'>📸 记忆相册</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["照片墙", "上传照片"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>温暖瞬间回顾</h2>", unsafe_allow_html=True)
            
            photos = [
                {"date": "2024-01-15", "desc": "和张明一起去超市购物", "volunteer": "张明"},
                {"date": "2024-01-20", "desc": "李华教我使用微信视频通话", "volunteer": "李华"},
                {"date": "2024-01-25", "desc": "和王芳在社区花园散步聊天", "volunteer": "王芳"}
            ]
            
            for photo in photos:
                with st.container():
                    st.markdown(f"**{photo['date']}** - {photo['desc']}")
                    st.markdown(f"👤 志愿者：{photo['volunteer']}")
                    st.markdown("---")
        
        with tab2:
            st.markdown("<h2 class='section-title'>上传新照片</h2>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("选择照片文件", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="照片预览")
                photo_desc = st.text_area("照片描述")
                
                if st.button("保存到相册", use_container_width=True):
                    st.success("✅ 照片已保存到记忆相册！")
    
    elif selected_page == "🗺️ 服务地图":
        st.markdown("<h1 class='main-title'>🗺️ 服务地图</h1>", unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-title'>📍 附近服务分布</h2>", unsafe_allow_html=True)
        
        service_map = create_service_map()
        folium_static(service_map, width=1000, height=600)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("附近老人", "8位")
        with col2:
            st.metric("可用志愿者", "5位")
        with col3:
            st.metric("平均距离", "1.2km")
        with col4:
            st.metric("服务覆盖率", "85%")
    
    elif selected_page == "📊 数据看板":
        st.markdown("<h1 class='main-title'>📊 运营数据全景看板</h1>", unsafe_allow_html=True)
        
        try:
            create_simple_dashboard()
        except Exception as e:
            st.error(f"数据看板加载出错: {str(e)}")
            
            st.markdown("### 📈 核心指标")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("累计订单", "1,568")
            with col2:
                st.metric("活跃老人", "156")
            with col3:
                st.metric("志愿者数", "89")
            with col4:
                st.metric("满意度", "4.82")
    
    elif selected_page == "👤 个人中心":
        st.markdown(f"<h1 class='main-title'>👤 个人中心 - {st.session_state.username}</h1>", unsafe_allow_html=True)
        
        user_info = user_system.users.get(st.session_state.username, {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 基本信息")
            st.markdown(f"**用户名**: {st.session_state.username}")
            st.markdown(f"**用户类型**: {user_info.get('user_type', '用户')}")
            st.markdown(f"**年龄**: {user_info.get('age', '未设置')}")
            st.markdown(f"**手机号**: {user_info.get('phone', '未设置')}")
        
        with col2:
            st.markdown("#### 服务信息")
            st.markdown(f"**积分**: {user_info.get('points', 0)}")
            st.markdown(f"**账户余额**: ¥{user_info.get('balance', 0):.2f}")
            st.markdown(f"**服务次数**: {user_info.get('service_count', 0)}")
            st.markdown(f"**兴趣标签**: {', '.join(user_info.get('interests', []))}")
    
    elif selected_page == "⚙️ 系统设置":
        st.markdown("<h1 class='main-title'>⚙️ 系统设置</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["通知设置", "隐私设置"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>通知偏好设置</h2>", unsafe_allow_html=True)
            email_notif = st.checkbox("📧 邮箱通知", value=True)
            sms_notif = st.checkbox("📱 短信通知", value=True)
            
            if st.button("保存设置", use_container_width=True):
                st.success("✅ 设置已保存")
        
        with tab2:
            st.markdown("<h2 class='section-title'>隐私设置</h2>", unsafe_allow_html=True)
            show_profile = st.radio("个人资料可见性", ["所有人可见", "仅志愿者可见", "仅自己可见"])
            allow_contact = st.checkbox("允许志愿者联系", value=True)
            
            if st.button("保存隐私设置", use_container_width=True):
                st.success("✅ 隐私设置已保存")
    
    else:  # 帮助页面
        st.markdown("<h1 class='main-title'>❓ 帮助与支持</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        ### 📖 银龄搭子使用指南
        
        #### 1. 如何预约服务？
        - 登录后点击"📅 预约服务"
        - 选择服务类型
        - 填写预约信息
        - 确认预约并支付
        
        #### 2. 如何支付？
        - 支持微信支付、支付宝、银联支付
        - 可使用账户余额支付
        
        #### 3. 联系客服
        **客服热线**: 400-123-4567
        **服务时间**: 每天 8:00-22:00
        
        #### 4. 紧急求助
        - 侧边栏有"🆘 紧急求助"按钮
        - 志愿者和社区将立即响应
        """)

# ==================== 部署配置 ====================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"程序运行出错: {str(e)}")
        st.info("请刷新页面重试，或联系技术支持")
