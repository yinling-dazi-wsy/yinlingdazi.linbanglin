# 银龄搭子 - 优化完整版
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

# ==================== 自定义CSS（适老化设计） ====================
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
        font-size: 24px !important;
        padding: 20px 30px !important;
        border-radius: 15px !important;
        margin: 15px !important;
    }
    
    /* 卡片样式 */
    .service-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 25px !important;
        border-radius: 15px !important;
        margin: 15px 0 !important;
        text-align: center !important;
        transition: transform 0.3s !important;
    }
    
    .service-card:hover {
        transform: scale(1.03) !important;
    }
    
    /* 紧急按钮 */
    .emergency-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        padding: 25px !important;
        border-radius: 15px !important;
        font-size: 28px !important;
        font-weight: bold !important;
        text-align: center !important;
        margin: 20px 0 !important;
        border: none !important;
    }
    
    /* 大字体输入框 */
    .big-input {
        font-size: 22px !important;
        padding: 18px !important;
        margin: 12px 0 !important;
    }
    
    /* 图表字体放大 */
    .stPlotlyChart, .stPyplot {
        font-size: 18px !important;
    }
    
    /* 侧边栏放大 */
    .sidebar .sidebar-content {
        font-size: 20px !important;
    }
    
    /* 进度条 */
    .stProgress > div > div > div > div {
        background-color: #FF9933 !important;
    }
    
    /* 成功提示 */
    .stAlert {
        font-size: 20px !important;
    }
    
    /* 图表容器 */
    .chart-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* 数据卡片 */
    .data-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
    }
    
    /* 支付卡片样式 */
    .payment-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .payment-method-card {
        border: 2px solid #ced4da;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .payment-method-card:hover {
        border-color: #FF9933;
        background-color: #FFF5E6;
    }
    
    .payment-method-card.selected {
        border-color: #FF9933;
        background-color: #FFF0D6;
    }
    
    .vip-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #8B4513;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    
    .commission-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 14px;
        display: inline-block;
        margin-left: 5px;
    }
    
    .fund-badge {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 14px;
        display: inline-block;
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
                "mutual_fund": 500.0,  # 银龄互助基金
                "total_commission": 1250.0,  # 总佣金收入
                "government_contracts": 3,  # 政府合作项目数
                "vip_members": 45,  # VIP会员数
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
        
        # 密码哈希存储
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # 根据用户类型设置合理的初始数据
        if user_type == "老人用户":
            points = 0
            service_count = 0
            rating = 0
            identity = "老人"
            balance = 100  # 新用户赠送100元体验金
            is_vip = False
        elif user_type == "志愿者":
            points = 100  # 注册赠送100积分
            service_count = 0
            rating = 5.0  # 初始评分5.0
            identity = "大学生" if age < 25 else "社区志愿者"
            balance = 0
            is_vip = False
        elif user_type == "家属/子女":
            points = 50
            service_count = 0
            rating = 0
            identity = "家属"
            balance = 200  # 家属用户赠送200元
            is_vip = False
        else:  # 社区管理员
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
            'balance': balance,  # 账户余额
            'total_spent': 0.0,  # 累计消费
            'commission_earned': 0.0,  # 佣金收入
            'vip_expiry': None,  # VIP到期时间
            'is_vip': is_vip,  # 是否是VIP
            'donation_total': 0.0  # 累计捐赠
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
            'expires': time.time() + 3600,  # 1小时有效期
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
        """通过邮箱查找用户（简化版，用手机号代替）"""
        for username, data in self.users.items():
            if data.get('phone') == email:  # 这里用手机号模拟邮箱
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
            'commission': amount * 0.1,  # 10%佣金
            'donation': amount * 0.005,  # 0.5%捐赠给互助基金
            'actual_amount': amount * 0.895  # 实际到志愿者账户
        }
        
        self.orders.append(order)
        self.save_orders()
        return order_id
    
    def process_payment(self, order_id, payment_method):
        """处理支付"""
        for order in self.orders:
            if order['order_id'] == order_id:
                if order['status'] == '待支付':
                    # 检查用户余额
                    user = self.users.get(order['username'])
                    if user['balance'] >= order['amount']:
                        # 扣款
                        user['balance'] -= order['amount']
                        user['total_spent'] += order['amount']
                        
                        # 更新订单状态
                        order['status'] = '已支付'
                        order['payment_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        order['payment_method'] = payment_method
                        
                        # 更新商业数据
                        self.business_data['mutual_fund'] += order['donation']
                        self.business_data['total_commission'] += order['commission']
                        self.business_data['orders_today'] += 1
                        self.business_data['revenue_today'] += order['amount']
                        self.business_data['commission_today'] += order['commission']
                        self.business_data['donation_today'] += order['donation']
                        
                        # 记录交易
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
                        
                        # 增加用户积分
                        user['points'] += int(order['amount'] / 10)  # 每10元1积分
                        
                        # 如果是VIP，增加额外积分
                        if user.get('is_vip', False):
                            user['points'] += int(order['amount'] / 5)  # VIP额外积分
                        
                        # 更新捐赠总额
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
            
            # 记录交易
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
            
            # VIP特权：充值赠送
            if self.users[username].get('is_vip', False) and amount >= 100:
                bonus = amount * 0.1  # VIP充值赠送10%
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
        
        # 订单信息卡片
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
        
        # 支付方式选择
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
                selection_class = "selected" if is_selected else ""
                
                if st.button(
                    f"{method['icon']} {method['name']}",
                    key=f"pay_method_{idx}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_payment_method = method['name']
                    st.rerun()
                
                st.caption(method['desc'])
        
        # 余额信息
        user_system = st.session_state.user_system
        username = st.session_state.username
        user_balance = user_system.users.get(username, {}).get('balance', 0)
        
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;'>
            <p><strong>账户余额：</strong> ¥{user_balance:.2f}</p>
            <p><strong>支付后余额：</strong> ¥{user_balance - amount:.2f if user_balance >= amount else '余额不足'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 支付按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ 确认支付", use_container_width=True, type="primary"):
                if user_balance >= amount:
                    success, message = user_system.process_payment(order_id, selected_method)
                    if success:
                        st.success("🎉 支付成功！")
                        st.balloons()
                        
                        # 显示支付成功详情
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
                        
                        # 等待3秒后返回首页
                        time.sleep(3)
                        st.session_state.page = "首页"
                        st.rerun()
                    else:
                        st.error(f"支付失败：{message}")
                else:
                    st.error("余额不足，请先充值")
                    
                    # 显示充值选项
                    st.markdown("#### 💰 立即充值")
                    recharge_amount = st.selectbox("选择充值金额", [50, 100, 200, 500, 1000])
                    
                    if st.button(f"充值 ¥{recharge_amount}", use_container_width=True):
                        if user_system.add_balance(username, recharge_amount, selected_method):
                            st.success(f"充值成功！当前余额：¥{user_system.users[username]['balance']:.2f}")
                            st.rerun()
                        else:
                            st.error("充值失败")
    
    @staticmethod
    def show_business_models():
        """展示商业模式"""
        st.markdown(f"<h2 class='section-title'>💼 商业模式</h2>", unsafe_allow_html=True)
        
        # 商业模式卡片
        models = [
            {
                "title": "💰 服务费收入",
                "icon": "💵",
                "desc": "基础陪伴服务10元/小时",
                "details": ["低价普惠服务", "按小时计费", "支持多种支付方式"],
                "color": "#28a745"
            },
            {
                "title": "🤝 商家返佣",
                "icon": "🏪",
                "desc": "与商超、药店合作，获得佣金",
                "details": ["合作商家100+", "平均佣金率15%", "月均返佣¥12,500"],
                "color": "#17a2b8"
            },
            {
                "title": "🌟 增值服务",
                "icon": "⭐",
                "desc": "套餐服务、节日礼包等",
                "details": ["定期陪伴套餐", "节日礼包配送", "健康管理服务"],
                "color": "#ffc107"
            },
            {
                "title": "🏛️ 政府购买服务",
                "icon": "🏛️",
                "desc": "承接政府为老服务项目",
                "details": ["已签约3个街道", "服务500+特困老人", "项目金额¥500,000+"],
                "color": "#6f42c1"
            }
        ]
        
        cols = st.columns(2)
        for idx, model in enumerate(models):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style='
                    background: {model['color']}10;
                    border: 2px solid {model['color']};
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0;
                '>
                    <div style='font-size: 36px; margin-bottom: 10px;'>{model['icon']}</div>
                    <h3>{model['title']}</h3>
                    <p>{model['desc']}</p>
                    <hr>
                    <ul style='padding-left: 20px;'>
                        {''.join([f'<li>{detail}</li>' for detail in model['details']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # 公益与商业结合
        st.markdown(f"<h3 class='section-title'>❤️ 公益与商业结合</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #FF9933 0%, #FF8C00 100%);
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
            '>
                <h3>🏆 志愿积分兑换</h3>
                <p>志愿者服务获得积分，可兑换：</p>
                <ul>
                    <li>🛍️ 合作商家礼品卡</li>
                    <li>🎫 电影票、演出票</li>
                    <li>🏨 酒店住宿优惠</li>
                    <li>✈️ 旅游套餐折扣</li>
                    <li>📱 手机充值券</li>
                </ul>
                <p><strong>当前积分池：</strong> 125,800 积分</p>
                <p><strong>已兑换：</strong> 89,450 积分</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
            '>
                <h3>🤲 银龄互助基金</h3>
                <p>每笔订单捐出0.5%，用于：</p>
                <ul>
                    <li>🏥 特困老人医疗救助</li>
                    <li>🎁 节日慰问礼包</li>
                    <li>🍚 免费午餐项目</li>
                    <li>🛋️ 适老化改造补贴</li>
                    <li>🎓 志愿者培训基金</li>
                </ul>
                <p><strong>基金总额：</strong> ¥{st.session_state.user_system.business_data['mutual_fund']:.2f}</p>
                <p><strong>已帮助：</strong> 156 位特困老人</p>
            </div>
            """, unsafe_allow_html=True)
        
        # VIP会员系统
        st.markdown(f"<h3 class='section-title'>👑 VIP会员系统</h3>", unsafe_allow_html=True)
        
        vip_features = [
            {"icon": "🎁", "title": "充值赠送", "desc": "充值赠送10%余额"},
            {"icon": "⭐", "title": "双倍积分", "desc": "消费获得双倍积分"},
            {"icon": "⚡", "title": "优先匹配", "desc": "优先匹配优质志愿者"},
            {"icon": "🆓", "title": "免佣服务", "desc": "部分服务免平台佣金"},
            {"icon": "🎫", "title": "专属礼包", "desc": "每月赠送专属礼包"},
            {"icon": "👨‍⚕️", "title": "健康顾问", "desc": "专属健康顾问服务"}
        ]
        
        cols = st.columns(3)
        for idx, feature in enumerate(vip_features):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='
                    background: #FFF5E6;
                    border: 1px solid #FFD699;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    text-align: center;
                '>
                    <div style='font-size: 30px;'>{feature['icon']}</div>
                    <h4>{feature['title']}</h4>
                    <p>{feature['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # VIP价格表
        st.markdown("#### 💎 VIP会员价格")
        vip_plans = [
            {"name": "月卡VIP", "price": "¥49.9", "period": "30天", "features": ["基础VIP权益", "适合短期体验"]},
            {"name": "季卡VIP", "price": "¥129", "period": "90天", "features": ["月卡权益", "赠送500积分", "9折优惠"]},
            {"name": "年卡VIP", "price": "¥399", "period": "365天", "features": ["季卡权益", "赠送2000积分", "专属顾问", "8折优惠"]}
        ]
        
        vip_cols = st.columns(3)
        for idx, plan in enumerate(vip_plans):
            with vip_cols[idx]:
                st.markdown(f"""
                <div style='
                    background: {'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' if idx == 2 else '#f8f9fa'};
                    border: 2px solid {'#FF8C00' if idx == 2 else '#dee2e6'};
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    margin: 10px 0;
                '>
                    <h3>{plan['name']}</h3>
                    <div style='font-size: 28px; font-weight: bold; color: #FF6B35;'>{plan['price']}</div>
                    <p>有效期：{plan['period']}</p>
                    <hr>
                    <ul style='text-align: left; padding-left: 20px;'>
                        {''.join([f'<li>{feature}</li>' for feature in plan['features']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"开通{plan['name']}", key=f"vip_{idx}", use_container_width=True):
                    st.info(f"正在开通{plan['name']}...")

# ==================== 数据初始化 ====================
@st.cache_data
def init_system_data():
    """初始化系统数据"""
    # 老人数据
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
    
    # 志愿者数据
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
    
    # 订单数据（用于图表） - 修复：使用字符串格式日期
    dates = pd.date_range(start='2024-01-01', end='2024-02-09', freq='D')
    # 转换为字符串格式 "YYYY-MM-DD"
    formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]
    
    orders_data = pd.DataFrame({
        '日期': formatted_dates,  # 使用字符串格式
        '订单数': np.random.randint(5, 25, len(dates)),
        '满意度': np.random.uniform(4.5, 5.0, len(dates))
    })
    
    return elderly_data, volunteer_data, orders_data

# ==================== 数据可视化函数（纯Streamlit版） ====================
def create_streamlit_dashboard():
    """纯Streamlit原生图表的数据看板 - 无需matplotlib"""
    
    # CSS样式
    st.markdown("""
    <style>
    .dashboard-title {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #FF8C42 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        padding: 15px !important;
        background: linear-gradient(135deg, #FFF5EB 0%, #FFE4CC 100%);
        border-radius: 15px !important;
        border: 2px solid #FF8C42 !important;
    }
    
    .chart-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #E0E0E0;
    }
    
    .chart-title {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #2D3748 !important;
        margin-bottom: 15px !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid #FF8C42 !important;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    
    @media (max-width: 768px) {
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 480px) {
        .metric-grid {
            grid-template-columns: 1fr;
        }
    }
    
    .metric-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 28px !important;
        font-weight: bold !important;
        margin: 5px 0 !important;
    }
    
    .metric-label {
        font-size: 16px !important;
        opacity: 0.9 !important;
    }
    
    .metric-change {
        font-size: 14px !important;
        margin-top: 5px !important;
        background: rgba(255, 255, 255, 0.2);
        padding: 3px 10px;
        border-radius: 10px;
        display: inline-block;
    }
    
    .big-number {
        font-size: 36px !important;
        font-weight: bold !important;
        color: #FF8C42 !important;
        text-align: center !important;
        margin: 20px 0 !important;
    }
    
    .data-label {
        font-size: 18px !important;
        font-weight: bold !important;
        margin: 10px 0 5px 0 !important;
    }
    
    .revenue-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    
    .donation-card {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    
    .vip-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #8B4513;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 标题
    st.markdown('<div class="dashboard-title">📊 银龄搭子数据看板</div>', unsafe_allow_html=True)
    
    # === 第1行：关键指标卡片 ===
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    
    user_system = st.session_state.user_system
    business_data = user_system.business_data
    
    metrics = [
        {"label": "累计服务", "value": "1,284", "change": "+128", "icon": "📈", "color": "#667eea"},
        {"label": "活跃老人", "value": "163", "change": "+12", "icon": "👵", "color": "#764ba2"},
        {"label": "志愿者数", "value": "89", "change": "+8", "icon": "👨‍⚕️", "color": "#4ECDC4"},
        {"label": "完成率", "value": "96%", "change": "+2%", "icon": "✅", "color": "#2ECC71"},
    ]
    
    for metric in metrics:
        st.markdown(f"""
        <div class="metric-item" style="background: linear-gradient(135deg, {metric['color']} 0%, {metric['color']}80 100%);">
            <div style="font-size: 24px; margin-bottom: 10px;">{metric['icon']}</div>
            <div class="metric-value">{metric['value']}</div>
            <div class="metric-label">{metric['label']}</div>
            <div class="metric-change">📈 {metric['change']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第2行：财务指标 ===
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    
    finance_metrics = [
        {"label": "今日收入", "value": f"¥{business_data['revenue_today']:.2f}", "change": f"+¥{business_data['revenue_today']*0.15:.2f}", "icon": "💰", "color": "#28a745"},
        {"label": "互助基金", "value": f"¥{business_data['mutual_fund']:.2f}", "change": f"+¥{business_data['donation_today']:.2f}", "icon": "❤️", "color": "#6c757d"},
        {"label": "累计佣金", "value": f"¥{business_data['total_commission']:.2f}", "change": f"+¥{business_data['commission_today']:.2f}", "icon": "💸", "color": "#17a2b8"},
        {"label": "VIP会员", "value": f"{business_data['vip_members']}人", "change": "+3", "icon": "👑", "color": "#FFD700"},
    ]
    
    for metric in finance_metrics:
        st.markdown(f"""
        <div class="metric-item" style="background: linear-gradient(135deg, {metric['color']} 0%, {metric['color']}80 100%);">
            <div style="font-size: 24px; margin-bottom: 10px;">{metric['icon']}</div>
            <div class="metric-value">{metric['value']}</div>
            <div class="metric-label">{metric['label']}</div>
            <div class="metric-change">📈 {metric['change']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第3行：订单趋势图（Streamlit原生折线图） ===
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 服务订单趋势（最近30天）</div>', unsafe_allow_html=True)
    
    # 准备趋势数据 - 简化版本
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    orders = np.random.randint(20, 50, 30)
    # 添加趋势
    orders = orders + np.arange(30) * 0.5
    orders = orders.astype(int)
    
    # 创建DataFrame
    trend_data = pd.DataFrame({
        '日期': dates,
        '订单数': orders
    })
    
    # 使用streamlit原生折线图
    st.line_chart(trend_data.set_index('日期')['订单数'], use_container_width=True)
    
    # 添加统计数据
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("最高", f"{orders.max()}单")
    with col2:
        st.metric("平均", f"{orders.mean():.1f}单/天")
    with col3:
        st.metric("增长", f"+{orders[-1]-orders[0]}单")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第4行：收入分布 ===
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💰 收入来源分布</div>', unsafe_allow_html=True)
    
    revenue_data = pd.DataFrame({
        '来源': ['服务费', '商家返佣', '增值服务', '政府项目'],
        '金额(万)': [28.5, 12.5, 8.2, 50.0],
        '占比(%)': [28.5, 12.5, 8.2, 50.0]
    })
    
    # 使用柱状图显示
    st.bar_chart(revenue_data.set_index('来源')['金额(万)'], use_container_width=True)
    
    # 显示详情
    for _, row in revenue_data.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{row['来源']}**")
        with col2:
            st.markdown(f"¥{row['金额(万)']}万")
        with col3:
            st.progress(row['占比(%)']/100)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第5行：两个并列图表 ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⭐ 志愿者评分分布</div>', unsafe_allow_html=True)
        
        # 评分数据 - 使用streamlit原生柱状图
        rating_data = pd.DataFrame({
            '评分区间': ['4.0-4.2', '4.3-4.5', '4.6-4.8', '4.9-5.0'],
            '人数': [8, 15, 42, 24]
        })
        
        st.bar_chart(rating_data.set_index('评分区间')['人数'], use_container_width=True)
        
        # 显示总数
        st.markdown(f'<div class="big-number">👥 {rating_data["人数"].sum()}人</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 服务需求分布</div>', unsafe_allow_html=True)
        
        # 服务数据 - 使用HTML/CSS创建简单的饼图
        services = {
            '日常陪伴': 35,
            '医疗协助': 25,
            '购物代办': 20,
            '学习辅导': 15,
            '其他服务': 5
        }
        
        total = sum(services.values())
        
        # 显示总数
        st.markdown(f'<div class="big-number">📋 {total}个需求</div>', unsafe_allow_html=True)
        
        # 使用进度条显示分布
        for service, value in services.items():
            percentage = (value / total) * 100
            col_left, col_right = st.columns([3, 1])
            with col_left:
                st.markdown(f'<div class="data-label">{service}</div>', unsafe_allow_html=True)
                st.progress(value/100)  # 使用百分比
            with col_right:
                st.markdown(f'**{value}** ({percentage:.1f}%)')
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第6行：年龄分布（使用DataFrame表格和进度条） ===
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">👵 老人年龄分布</div>', unsafe_allow_html=True)
    
    # 使用您提供的数据
    age_data = pd.DataFrame({
        '年龄区间': ['60-65岁', '66-70岁', '71-75岁', '76-80岁', '81-85岁'],
        '人数': [25, 38, 42, 28, 18],
        '百分比 (%)': [23, 38, 42, 28, 18]  # 根据您提供的百分比
    })
    
    # 使用streamlit的数据表显示
    st.dataframe(
        age_data,
        column_config={
            "年龄区间": st.column_config.TextColumn("年龄区间", width="medium"),
            "人数": st.column_config.NumberColumn("人数", width="small"),
            "百分比 (%)": st.column_config.ProgressColumn(
                "百分比 (%)",
                format="%d%%",
                min_value=0,
                max_value=100,
                width="large"
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    
    # 使用柱状图再次显示
    st.bar_chart(age_data.set_index('年龄区间')['人数'], use_container_width=True)
    
    # 显示总数
    total_elders = age_data['人数'].sum()
    st.markdown(f'<div class="big-number">👵 共有 {total_elders} 位老人</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第7行：志愿者服务排行（使用表格） ===
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🏆 志愿者服务排行</div>', unsafe_allow_html=True)
    
    # 志愿者数据
    volunteer_rank = pd.DataFrame({
        '志愿者': ['张明', '李华', '王芳', '陈伟', '刘婷', '周杰', '吴琳'],
        '服务次数': [45, 32, 56, 28, 39, 42, 38],
        '评分': [4.9, 4.7, 5.0, 4.8, 4.6, 4.9, 5.0],
        '服务时长': [120, 85, 156, 75, 108, 125, 95],
        '收入': [5400, 3840, 6720, 3360, 4680, 5040, 4560]
    })
    
    # 按服务次数排序
    volunteer_rank = volunteer_rank.sort_values('服务次数', ascending=False)
    
    # 显示表格
    st.dataframe(
        volunteer_rank,
        column_config={
            "志愿者": st.column_config.TextColumn("志愿者", width="medium"),
            "服务次数": st.column_config.NumberColumn("服务次数", width="small"),
            "评分": st.column_config.NumberColumn("评分", format="%.1f ⭐", width="small"),
            "服务时长": st.column_config.NumberColumn("服务时长（小时）", width="small"),
            "收入": st.column_config.NumberColumn("收入（元）", format="¥%d", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # 添加统计
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("最高服务", f"{volunteer_rank['服务次数'].max()}次")
    with col2:
        st.metric("平均评分", f"{volunteer_rank['评分'].mean():.1f}")
    with col3:
        st.metric("总收入", f"¥{volunteer_rank['收入'].sum():.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === 第8行：实时统计 ===
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 实时统计数据</div>', unsafe_allow_html=True)
    
    realtime_col1, realtime_col2, realtime_col3, realtime_col4 = st.columns(4)
    
    with realtime_col1:
        st.metric("今日订单", f"{business_data['orders_today']}", "+3")
    with realtime_col2:
        st.metric("在线志愿者", "12", "在线")
    with realtime_col3:
        st.metric("待处理", "5", "-2")
    with realtime_col4:
        st.metric("今日完成", "23", "已完成")
    
    # 添加说明
    st.info("💡 所有数据每5分钟自动更新，图表支持触摸操作")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 地图功能 ====================
def create_service_map():
    """创建服务地图"""
    # 模拟坐标（上海市中心）
    base_lat, base_lng = 31.2304, 121.4737
    
    # 创建地图
    m = folium.Map(location=[base_lat, base_lng], zoom_start=12, control_scale=True)
    
    # 添加老人位置（蓝色标记）
    elder_icons = ['user', 'home', 'heart', 'star', 'info']
    elder_colors = ['blue', 'purple', 'darkblue', 'cadetblue', 'darkpurple']
    
    for i in range(5):
        lat = base_lat + random.uniform(-0.05, 0.05)
        lng = base_lng + random.uniform(-0.05, 0.05)
        folium.Marker(
            [lat, lng],
            popup=f"<b>老人{i+1}</b><br>需求：购物陪伴<br>距离：{random.uniform(0.5, 2.0):.1f}km",
            tooltip=f"点击查看老人{i+1}信息",
            icon=folium.Icon(color=elder_colors[i], icon=elder_icons[i], prefix='fa')
        ).add_to(m)
    
    # 添加志愿者位置（绿色标记）
    for i in range(3):
        lat = base_lat + random.uniform(-0.03, 0.03)
        lng = base_lng + random.uniform(-0.03, 0.03)
        folium.Marker(
            [lat, lng],
            popup=f"<b>志愿者{i+1}</b><br>评分：{4.5+random.random():.1f}<br>可服务：聊天/购物",
            tooltip=f"点击查看志愿者{i+1}信息",
            icon=folium.Icon(color='green', icon='heart', prefix='fa')
        ).add_to(m)
    
    # 添加社区中心（红色标记）
    folium.Marker(
        [base_lat, base_lng],
        popup="<b>社区服务中心</b><br>地址：某某路123号<br>电话：400-123-4567",
        tooltip="社区服务中心",
        icon=folium.Icon(color='red', icon='flag', prefix='fa')
    ).add_to(m)
    
    # 添加圆圈表示服务范围
    folium.Circle(
        location=[base_lat, base_lng],
        radius=2000,  # 2公里
        color='orange',
        fill=True,
        fill_color='orange',
        fill_opacity=0.2,
        popup="2公里服务范围"
    ).add_to(m)
    
    return m

# ==================== 主程序 ====================
def main():
    # 初始化用户系统和数据
    user_system = UserSystem()
    elderly_data, volunteer_data, orders_data = init_system_data()
    
    # 存储用户系统到会话状态
    st.session_state.user_system = user_system
    
    # 会话状态初始化
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
    
    # ==================== 密码重置页面 ====================
    if st.session_state.show_password_reset:
        st.markdown("<h1 class='main-title'>🔐 密码重置</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["申请重置", "重置密码"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>申请密码重置</h2>", unsafe_allow_html=True)
            reset_phone = st.text_input("📱 请输入注册手机号", placeholder="请输入11位手机号")
            
            if st.button("发送重置链接", use_container_width=True, type="primary"):
                user = user_system.find_user_by_email(reset_phone)
                if user:
                    token = user_system.generate_reset_token(user)
                    # 在实际应用中，这里应该发送邮件或短信
                    st.success(f"✅ 重置令牌已生成（演示用）：{token[:16]}...")
                    st.info("请复制上方令牌，在'重置密码'页面使用")
                else:
                    st.error("手机号未注册")
        
        with tab2:
            st.markdown("<h2 class='section-title'>重置密码</h2>", unsafe_allow_html=True)
            reset_token = st.text_input("🔑 请输入重置令牌", placeholder="请输入32位重置令牌")
            new_password = st.text_input("🔐 新密码", type="password", placeholder="至少6位字符")
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
    
    # ==================== 登录/注册页面 ====================
    if not st.session_state.logged_in:
        st.markdown("<h1 class='main-title'>👵 银龄搭子 · 欢迎您</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 登录", "📝 注册"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>用户登录</h2>", unsafe_allow_html=True)
            
            login_col1, login_col2 = st.columns([2, 1])
            with login_col1:
                login_username = st.text_input("👤 用户名", key="login_user", 
                                              placeholder="请输入用户名")
                login_password = st.text_input("🔑 密码", type="password", 
                                              key="login_pass", placeholder="请输入密码")
                
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
                
                # 忘记密码链接
                st.markdown("---")
                if st.button("忘记密码？", use_container_width=True):
                    st.session_state.show_password_reset = True
                    st.rerun()
            
            with login_col2:
                st.markdown("#### 💡 温馨提示")
                st.info("""
                - 老人账号：查看服务、预约
                - 志愿者账号：接单、上传照片
                - 家属账号：代老人预约
                - 管理员账号：数据管理
                """)
        
        with tab2:
            st.markdown("<h2 class='section-title'>新用户注册</h2>", unsafe_allow_html=True)
            
            reg_col1, reg_col2 = st.columns(2)
            with reg_col1:
                reg_username = st.text_input("👤 设置用户名", placeholder="3-10位字符")
                reg_password = st.text_input("🔑 设置密码", type="password", placeholder="至少6位")
                reg_password2 = st.text_input("✅ 确认密码", type="password")
                reg_phone = st.text_input("📱 手机号码", placeholder="11位手机号")
            
            with reg_col2:
                reg_type = st.selectbox("👥 用户类型", 
                                       ["老人用户", "志愿者", "家属/子女", "社区管理员"])
                reg_address = st.text_input("📍 居住地址", placeholder="详细地址便于服务")
                reg_age = st.number_input("🎂 年龄", min_value=0, max_value=120, value=60)
                reg_interests = st.multiselect("❤️ 兴趣爱好", 
                                              ["园艺", "书法", "戏曲", "烹饪", "散步", 
                                               "聊天", "手工", "音乐", "运动", "阅读", "养生"])
            
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
        
        st.markdown("---")
        st.markdown("#### 🎯 平台特色")
        cols = st.columns(4)
        features = [
            ("🤝 智能匹配", "根据兴趣、位置智能推荐"),
            ("💳 便捷支付", "多种支付方式，支持余额支付"),
            ("📸 记忆留存", "记录温暖陪伴时光"),
            ("💰 多元商业模式", "可持续的公益+商业模式")
        ]
        
        for col, (title, desc) in zip(cols, features):
            with col:
                st.markdown(f"**{title}**")
                st.caption(desc)
        
        return
    
    # ==================== 支付页面 ====================
    if st.session_state.show_payment and st.session_state.current_order:
        PaymentSystem.show_payment_page(
            st.session_state.current_order['order_id'],
            st.session_state.current_order['amount'],
            st.session_state.current_order['service_type']
        )
        
        # 返回按钮
        if st.button("返回预约", use_container_width=True):
            st.session_state.show_payment = False
            st.rerun()
        
        return
    
    # ==================== 主界面（已登录） ====================
    # 侧边栏
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.username}")
        user_data = user_system.users.get(st.session_state.username, {})
        user_type_display = user_data.get('user_type', '用户')
        identity = user_data.get('identity', '会员')
        st.markdown(f"**身份**: {user_type_display} ({identity})")
        
        # 显示VIP标识
        if user_data.get('is_vip', False):
            st.markdown('<span class="vip-badge">👑 VIP会员</span>', unsafe_allow_html=True)
        
        # 显示余额
        balance = user_data.get('balance', 0)
        st.markdown(f"**余额**: ¥{balance:.2f}")
        
        # 显示积分
        points = user_data.get('points', 0)
        st.markdown(f"**积分**: {points} 分")
        
        # 用户菜单（添加了支付和商业模式）
        menu_options = ["🏠 首页", "🤝 智能匹配", "📅 预约服务", "💰 支付中心", 
                       "💼 商业模式", "📸 记忆相册", "🗺️ 服务地图", "📊 数据看板", 
                       "👤 个人中心", "⚙️ 系统设置", "❓ 帮助"]
        
        selected_page = st.radio("导航菜单", menu_options)
        
        # 紧急求助按钮
        st.markdown("---")
        emergency_col1, emergency_col2 = st.columns(2)
        with emergency_col1:
            if st.button("🆘 紧急求助", use_container_width=True, type="primary"):
                st.success("紧急求助已发送！志愿者和社区将立即响应。")
        with emergency_col2:
            if st.button("📞 联系家属", use_container_width=True):
                emergency_contact = user_data.get('emergency_contact', '无')
                st.info(f"正在联系家属：{emergency_contact}")
        
        # 快捷充值按钮
        st.markdown("---")
        if st.button("💰 快捷充值", use_container_width=True):
            st.session_state.page = "支付中心"
            st.rerun()
        
        # 登出按钮
        st.markdown("---")
        if st.button("退出登录", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.show_payment = False
            st.session_state.current_order = None
            st.rerun()
    
    # ==================== 首页 ====================
    if selected_page == "🏠 首页":
        st.markdown(f"<h1 class='main-title'>👵 欢迎回来，{st.session_state.username}！</h1>", 
                   unsafe_allow_html=True)
        
        # 个性化问候
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            greeting = "🌅 早上好！今天天气不错，适合出门走走。"
        elif current_hour < 18:
            greeting = "☀️ 下午好！阳光正好，要不要约个志愿者聊聊天？"
        else:
            greeting = "🌙 晚上好！今天过得怎么样？"
        
        st.markdown(f"### {greeting}")
        
        # 余额和积分概览
        user_info = user_system.users.get(st.session_state.username, {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 账户余额", f"¥{user_info.get('balance', 0):.2f}")
        with col2:
            st.metric("⭐ 我的积分", f"{user_info.get('points', 0)} 分")
        with col3:
            if user_info.get('is_vip', False):
                st.metric("👑 VIP会员", "有效期内", "VIP")
            else:
                st.metric("👑 VIP会员", "立即开通", "免费试用")
        
        # 服务入口（大卡片设计）
        st.markdown("<h2 class='section-title'>🛠️ 选择您需要的服务</h2>", 
                   unsafe_allow_html=True)
        
        services = [
            {"icon": "🛒", "name": "陪逛代购", "desc": "超市/菜场/药店陪伴购物", "color": "#FF9933", "price": "10元/小时"},
            {"icon": "📱", "name": "手机教学", "desc": "微信/挂号/防诈骗一对一教学", "color": "#4ECDC4", "price": "10元/小时"},
            {"icon": "🛠️", "name": "便民服务", "desc": "取快递/缴费/简单维修协助", "color": "#3498DB", "price": "8元/小时"},
            {"icon": "🥬", "name": "社区团购", "desc": "长辈专享商品配送到家", "color": "#9B59B6", "price": "免费+商品费"},
            {"icon": "💬", "name": "聊天陪伴", "desc": "陪伴聊天散步缓解孤独", "color": "#E67E22", "price": "5元/小时"},
            {"icon": "🏥", "name": "医院陪诊", "desc": "陪同就医取药", "color": "#2ECC71", "price": "15元/小时"}
        ]
        
        cols = st.columns(3)
        for idx, service in enumerate(services):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='
                    background: {service['color']};
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    margin: 10px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                '>
                    <div style='font-size: 40px; margin-bottom: 10px;'>{service['icon']}</div>
                    <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>{service['name']}</div>
                    <div style='font-size: 18px; margin-bottom: 10px;'>{service['desc']}</div>
                    <div style='font-size: 16px; background: rgba(255,255,255,0.2); padding: 5px; border-radius: 5px;'>
                        💰 {service['price']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"选择 {service['name']}", key=f"service_{idx}", 
                           use_container_width=True):
                    st.session_state.selected_service = service['name']
                    st.success(f"已选择{service['name']}，请继续填写预约信息")
        
        # 推荐志愿者
        st.markdown("<h2 class='section-title'>🤝 为您推荐的志愿者</h2>", 
                   unsafe_allow_html=True)
        
        # 显示前3名志愿者
        top_volunteers = volunteer_data.nlargest(3, '评分')
        for idx, volunteer in top_volunteers.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.markdown(f"<div style='text-align: center; font-size: 40px;'>👤</div>", 
                               unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{volunteer['姓名']}** ⭐{volunteer['评分']}")
                    st.markdown(f"📍 {volunteer['服务区域']} | 📏 {volunteer['距离(km)']}km")
                    st.markdown(f"🛠️ {volunteer['擅长服务'].split(',')[0]}")
                    st.markdown(f"💰 时薪：12-18元")
                with col3:
                    if st.button("选择搭子", key=f"rec_{idx}", use_container_width=True):
                        st.success(f"已选择 {volunteer['姓名']} 作为您的搭子！")
                st.markdown("---")
    
    # ==================== 智能匹配页面 ====================
    elif selected_page == "🤝 智能匹配":
        st.markdown("<h1 class='main-title'>🤖 智能匹配系统</h1>", unsafe_allow_html=True)
        
        with st.form("匹配设置", border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👵 匹配条件")
                service_type = st.selectbox("服务类型", 
                    ["陪逛代购", "手机教学", "便民服务", "社区团购", "聊天陪伴", "医院陪诊"])
                
                priority = st.radio("匹配优先级", 
                    ["智能推荐", "距离最近", "评分最高", "兴趣最匹配", "服务次数最多"])
                
                max_distance = st.slider("最大距离（公里）", 0.5, 5.0, 2.0, 0.5)
            
            with col2:
                st.markdown("#### 🎯 个性化设置")
                interests = st.multiselect("兴趣标签", 
                    ["园艺", "书法", "戏曲", "烹饪", "散步", "聊天", "手工", "音乐", "运动", "阅读", "养生"],
                    default=["园艺", "聊天"])
                
                language_pref = st.multiselect("语言偏好", 
                    ["普通话", "上海话", "其他方言", "英语"], default=["普通话", "上海话"])
                
                time_pref = st.selectbox("偏好时间", 
                    ["上午", "中午", "下午", "晚上", "全天"])
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                match_btn = st.form_submit_button("🚀 开始智能匹配", use_container_width=True, type="primary")
        
        if match_btn:
            st.markdown("<h2 class='section-title'>🎯 匹配结果</h2>", unsafe_allow_html=True)
            
            # 模拟匹配算法
            matched = volunteer_data.copy()
            matched['匹配分'] = 0
            
            for idx, row in matched.iterrows():
                score = 0
                
                # 距离评分
                if row['距离(km)'] <= max_distance:
                    score += 40 - row['距离(km)'] * 10
                
                # 评分加成
                score += row['评分'] * 10
                
                # 服务次数加成
                score += row['服务次数'] * 0.5
                
                matched.loc[idx, '匹配分'] = score
            
            # 显示结果
            top_matches = matched.nlargest(3, '匹配分')
            
            for rank, (_, volunteer) in enumerate(top_matches.iterrows(), 1):
                with st.expander(f"第{rank}名: {volunteer['姓名']} (匹配分: {volunteer['匹配分']:.1f})", expanded=True):
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
                    st.markdown(f"**兴趣标签**: {volunteer['兴趣标签']}")
                    
                    # 计算服务价格
                    base_price = 10  # 基础价格10元/小时
                    if volunteer['身份'] == '退休医生' and '医院陪诊' in volunteer['擅长服务']:
                        price = 15
                    elif volunteer['评分'] >= 4.8:
                        price = 12
                    else:
                        price = base_price
                    
                    st.markdown(f"**预估价格**: ¥{price}/小时")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        duration = st.selectbox(f"选择时长", [1, 2, 3, 4], key=f"dur_{rank}", format_func=lambda x: f"{x}小时")
                    with col2:
                        total_price = price * duration
                        st.markdown(f"**总价**: ¥{total_price}")
                    
                    if st.button(f"选择 {volunteer['姓名']}", key=f"select_{rank}", 
                               use_container_width=True, type="primary"):
                        # 创建订单
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
    
    # ==================== 预约服务页面 ====================
    elif selected_page == "📅 预约服务":
        st.markdown("<h1 class='main-title'>📅 服务预约</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["1️⃣ 选择服务", "2️⃣ 填写信息", "3️⃣ 确认预约"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>🎯 第一步：选择服务类型</h2>", 
                       unsafe_allow_html=True)
            
            service_options = {
                "陪逛代购": {"icon": "🛒", "desc": "超市/菜场/药店陪伴购物", "price": 10},
                "手机教学": {"icon": "📱", "desc": "微信/挂号/防诈骗一对一教学", "price": 10},
                "便民服务": {"icon": "🛠️", "desc": "取快递/缴费/简单维修协助", "price": 8},
                "社区团购": {"icon": "🥬", "desc": "长辈专享商品配送到家", "price": 0},
                "聊天陪伴": {"icon": "💬", "desc": "陪伴聊天散步缓解孤独", "price": 5},
                "医院陪诊": {"icon": "🏥", "desc": "陪同就医、取药、问诊", "price": 15}
            }
            
            selected_service = st.radio(
                "请选择服务类型：",
                options=list(service_options.keys()),
                format_func=lambda x: f"{service_options[x]['icon']} {x} - {service_options[x]['desc']} - ¥{service_options[x]['price']}/小时",
                horizontal=False
            )
            
            if selected_service:
                st.success(f"✅ 已选择：{selected_service}")
                st.info(f"💡 {service_options[selected_service]['desc']}")
        
        with tab2:
            st.markdown("<h2 class='section-title'>📝 第二步：填写预约信息</h2>", 
                       unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                service_date = st.date_input("📅 预约日期", 
                    min_value=datetime.date.today(),
                    max_value=datetime.date.today() + datetime.timedelta(days=30))
                
                time_slot = st.selectbox("⏰ 服务时段", 
                    ["9:00-11:00 (上午)", "11:00-13:00 (中午)", 
                     "13:00-15:00 (下午)", "15:00-17:00 (傍晚)", 
                     "17:00-19:00 (晚上)"])
                
                duration = st.select_slider("⏱️ 服务时长", 
                    options=["1小时", "2小时", "3小时", "4小时"], value="2小时")
            
            with col2:
                address = st.text_input("📍 服务地址", 
                    value=user_system.users.get(st.session_state.username, {}).get('address', ''),
                    placeholder="请输入详细地址")
                
                contact_person = st.text_input("👤 联系人", 
                    placeholder="请输入联系人姓名")
                
                contact_phone = st.text_input("📱 联系电话", 
                    value=user_system.users.get(st.session_state.username, {}).get('phone', ''),
                    placeholder="请输入11位手机号码")
            
            special_notes = st.text_area("📋 特殊说明（选填）", 
                placeholder="例如：需要轮椅协助、对某些食物过敏、有宠物等",
                height=100)
        
        with tab3:
            st.markdown("<h2 class='section-title'>✅ 第三步：确认预约并支付</h2>", 
                       unsafe_allow_html=True)
            
            if 'selected_service' in locals():
                # 计算价格
                price_per_hour = service_options[selected_service]['price']
                hours = int(duration.split('小时')[0])
                total_amount = price_per_hour * hours
                
                # VIP折扣
                user_info = user_system.users.get(st.session_state.username, {})
                discount = 0.9 if user_info.get('is_vip', False) else 1.0
                final_amount = total_amount * discount
                
                st.markdown(f"""
                <div class='payment-card'>
                    <h3>📋 订单详情</h3>
                    
                    <h4>基本信息：</h4>
                    <ul>
                        <li>🛠️ 服务类型：{selected_service}</li>
                        <li>📅 预约日期：{service_date}</li>
                        <li>⏰ 服务时段：{time_slot}</li>
                        <li>⏱️ 服务时长：{duration}</li>
                        <li>💰 单价：¥{price_per_hour}/小时</li>
                    </ul>
                    
                    <h4>联系信息：</h4>
                    <ul>
                        <li>📍 服务地址：{address}</li>
                        <li>👤 联系人：{contact_person if contact_person else '未填写'}</li>
                        <li>📱 联系电话：{contact_phone if contact_phone else '未填写'}</li>
                    </ul>
                    
                    <h4>费用明细：</h4>
                    <ul>
                        <li>基础服务费：¥{total_amount:.2f}</li>
                        {f'<li>VIP折扣：{int((1-discount)*100)}% 优惠</li>' if discount < 1 else ''}
                        <li>平台佣金：¥{final_amount*0.1:.2f} <span class="commission-badge">10%</span></li>
                        <li>互助基金：¥{final_amount*0.005:.2f} <span class="fund-badge">0.5%捐赠</span></li>
                        <li><strong>总计：¥{final_amount:.2f}</strong></li>
                    </ul>
                    
                    <p><em>💝 您的支付将为特困老人带来温暖，感谢您的支持！</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                special_notes_display = special_notes if special_notes else '无特殊说明'
                st.markdown(f"**特殊说明：** {special_notes_display}")
                
                agree_terms = st.checkbox("✅ 我已阅读并同意《服务协议》和《隐私政策》")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💰 确认并支付", use_container_width=True, type="primary", 
                               disabled=not agree_terms):
                        # 创建订单
                        order_id = user_system.create_order(
                            st.session_state.username,
                            selected_service,
                            duration,
                            final_amount
                        )
                        
                        st.session_state.current_order = {
                            'order_id': order_id,
                            'amount': final_amount,
                            'service_type': selected_service,
                            'duration': duration
                        }
                        
                        st.session_state.show_payment = True
                        st.rerun()
                
                if not agree_terms:
                    st.warning("请先同意服务协议")
    
    # ==================== 支付中心页面 ====================
    elif selected_page == "💰 支付中心":
        st.markdown("<h1 class='main-title'>💰 支付中心</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["💳 账户余额", "📋 订单管理", "📊 交易记录", "🔄 充值中心"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>💳 我的账户</h2>", unsafe_allow_html=True)
            
            user_info = user_system.users.get(st.session_state.username, {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 20px; border-radius: 15px; text-align: center;'>
                    <div style='font-size: 24px;'>💰</div>
                    <div style='font-size: 28px; font-weight: bold;'>¥{user_info.get('balance', 0):.2f}</div>
                    <div>账户余额</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%); 
                            color: white; padding: 20px; border-radius: 15px; text-align: center;'>
                    <div style='font-size: 24px;'>⭐</div>
                    <div style='font-size: 28px; font-weight: bold;'>{user_info.get('points', 0)}</div>
                    <div>我的积分</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if user_info.get('is_vip', False):
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                                color: #8B4513; padding: 20px; border-radius: 15px; text-align: center;'>
                        <div style='font-size: 24px;'>👑</div>
                        <div style='font-size: 28px; font-weight: bold;'>VIP会员</div>
                        <div>有效期至：{user_info.get('vip_expiry', '长期有效')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #E0E0E0 0%, #BDBDBD 100%); 
                                color: #666; padding: 20px; border-radius: 15px; text-align: center;'>
                        <div style='font-size: 24px;'>👑</div>
                        <div style='font-size: 28px; font-weight: bold;'>普通会员</div>
                        <div>升级VIP享更多特权</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 消费统计
            st.markdown("<h3 class='section-title'>📊 消费统计</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("累计消费", f"¥{user_info.get('total_spent', 0):.2f}")
            with col2:
                st.metric("累计捐赠", f"¥{user_info.get('donation_total', 0):.2f}")
            with col3:
                st.metric("服务次数", f"{user_info.get('service_count', 0)}次")
            with col4:
                st.metric("节省金额", f"¥{user_info.get('total_spent', 0)*0.1:.2f}", "+10%返现")
        
        with tab2:
            st.markdown("<h2 class='section-title'>📋 我的订单</h2>", unsafe_allow_html=True)
            
            orders = user_system.get_user_orders(st.session_state.username)
            
            if orders:
                for order in reversed(orders):  # 显示最新的订单在前
                    status_color = {
                        '待支付': '#F39C12',
                        '已支付': '#2ECC71',
                        '已完成': '#3498DB',
                        '已取消': '#E74C3C'
                    }.get(order['status'], '#95A5A6')
                    
                    with st.expander(f"订单号：{order['order_id']} | 状态：{order['status']}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**服务类型**: {order['service_type']}")
                            st.markdown(f"**服务时长**: {order['duration']}")
                            st.markdown(f"**创建时间**: {order['create_time']}")
                        with col2:
                            st.markdown(f"**订单金额**: ¥{order['amount']:.2f}")
                            st.markdown(f"**支付方式**: {order.get('payment_method', '未支付')}")
                            st.markdown(f"**支付时间**: {order.get('payment_time', '未支付')}")
                        
                        # 费用明细
                        st.markdown("**费用明细**:")
                        st.markdown(f"- 服务费：¥{order['actual_amount']:.2f}")
                        st.markdown(f"- 平台佣金：¥{order['commission']:.2f}")
                        st.markdown(f"- 互助基金：¥{order['donation']:.2f}")
                        
                        # 订单操作
                        if order['status'] == '待支付':
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("支付", key=f"pay_{order['order_id']}", use_container_width=True):
                                    st.session_state.current_order = order
                                    st.session_state.show_payment = True
                                    st.rerun()
                            with col2:
                                if st.button("取消", key=f"cancel_{order['order_id']}", use_container_width=True):
                                    order['status'] = '已取消'
                                    user_system.save_orders()
                                    st.success("订单已取消")
                                    st.rerun()
            else:
                st.info("暂无订单记录")
        
        with tab3:
            st.markdown("<h2 class='section-title'>📊 交易记录</h2>", unsafe_allow_html=True)
            
            transactions = user_system.get_user_transactions(st.session_state.username)
            
            if transactions:
                for tx in reversed(transactions):  # 显示最新的交易在前
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            st.markdown(f"**{tx['type']}**")
                            st.caption(f"交易号：{tx['transaction_id']}")
                            if 'order_id' in tx:
                                st.caption(f"订单号：{tx['order_id']}")
                        with col2:
                            amount_color = "#2ECC71" if tx['type'] == '充值' else "#E74C3C"
                            amount_prefix = "+" if tx['type'] == '充值' else "-"
                            st.markdown(f"<span style='color: {amount_color}; font-weight: bold;'>{amount_prefix}¥{tx['amount']:.2f}</span>", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"`{tx['payment_method']}`")
                        with col4:
                            st.markdown(f"{tx['time']}")
                        st.markdown("---")
            else:
                st.info("暂无交易记录")
        
        with tab4:
            st.markdown("<h2 class='section-title'>🔄 充值中心</h2>", unsafe_allow_html=True)
            
            # 充值金额选项
            st.markdown("#### 💰 选择充值金额")
            recharge_options = [50, 100, 200, 500, 1000]
            
            cols = st.columns(5)
            for idx, amount in enumerate(recharge_options):
                with cols[idx]:
                    if st.button(f"¥{amount}", key=f"recharge_{amount}", use_container_width=True):
                        st.session_state.recharge_amount = amount
            
            # 自定义充值
            st.markdown("---")
            custom_amount = st.number_input("或输入自定义金额", min_value=10, max_value=5000, value=100, step=50)
            
            # 支付方式选择
            st.markdown("#### 💳 选择支付方式")
            payment_method = st.radio("支付方式", ["微信支付", "支付宝", "银联支付"], horizontal=True)
            
            # VIP充值优惠
            user_info = user_system.users.get(st.session_state.username, {})
            if user_info.get('is_vip', False):
                st.success(f"👑 VIP专属优惠：充值 ¥{custom_amount:.0f} 赠送 ¥{custom_amount*0.1:.2f}！")
            
            # 确认充值
            if st.button("立即充值", use_container_width=True, type="primary"):
                recharge_amount = custom_amount
                if user_info.get('is_vip', False):
                    recharge_amount = custom_amount * 1.1  # VIP赠送10%
                
                if user_system.add_balance(st.session_state.username, recharge_amount, payment_method):
                    st.success(f"✅ 充值成功！¥{custom_amount:.2f} 已到账" + 
                              (f"，VIP赠送 ¥{custom_amount*0.1:.2f}" if user_info.get('is_vip', False) else ""))
                    st.info(f"当前余额：¥{user_system.users[st.session_state.username]['balance']:.2f}")
                    st.rerun()
                else:
                    st.error("充值失败，请稍后重试")
    
    # ==================== 商业模式页面 ====================
    elif selected_page == "💼 商业模式":
        st.markdown("<h1 class='main-title'>💼 银龄搭子商业模式</h1>", unsafe_allow_html=True)
        
        PaymentSystem.show_business_models()
    
    # ==================== 记忆相册页面 ====================
    elif selected_page == "📸 记忆相册":
        st.markdown("<h1 class='main-title'>📸 记忆相册</h1>", unsafe_allow_html=True)
        
        # 创建选项卡
        tab1, tab2, tab3 = st.tabs(["🖼️ 照片墙", "📅 时间线", "📤 上传照片"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>温暖瞬间回顾</h2>", 
                       unsafe_allow_html=True)
            
            # 模拟照片数据
            photos = [
                {"date": "2024-01-15", "desc": "和张明一起去超市购物，买了新鲜蔬菜水果", 
                 "volunteer": "张明", "service": "陪逛代购", "likes": 12},
                {"date": "2024-01-20", "desc": "李华教我使用微信视频通话，现在可以和孙子视频了！", 
                 "volunteer": "李华", "service": "手机教学", "likes": 18},
                {"date": "2024-01-25", "desc": "和王芳在社区花园散步聊天，欣赏春天的花朵", 
                 "volunteer": "王芳", "service": "聊天陪伴", "likes": 15},
                {"date": "2024-01-30", "desc": "陈伟帮忙取了快递，还帮我搬上楼，真是个好孩子", 
                 "volunteer": "陈伟", "service": "便民服务", "likes": 10},
                {"date": "2024-02-05", "desc": "社区团购的蔬菜到了，刘婷帮忙配送到家", 
                 "volunteer": "刘婷", "service": "社区团购", "likes": 8},
                {"date": "2024-02-08", "desc": "周杰陪同去医院检查，全程细心照顾", 
                 "volunteer": "周杰", "service": "医院陪诊", "likes": 20}
            ]
            
            # 显示照片网格
            cols = st.columns(3)
            for idx, photo in enumerate(photos):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style='
                        border: 2px solid #FF9933;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 10px 0;
                        background: white;
                    '>
                        <div style='font-size: 20px; font-weight: bold; color: #FF9933;'>
                            {photo['date']}
                        </div>
                        <div style='font-size: 18px; margin: 10px 0;'>
                            {photo['desc']}
                        </div>
                        <div style='font-size: 16px; color: #666;'>
                            👤 {photo['volunteer']} | 🛠️ {photo['service']} | ❤️ {photo['likes']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🔄 加载更多回忆", use_container_width=True):
                st.success("正在加载更多温暖瞬间...")
        
        with tab2:
            st.markdown("<h2 class='section-title'>时间线回顾</h2>", 
                       unsafe_allow_html=True)
            
            # 创建简单的时间线
            for photo in photos:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{photo['date']}**")
                        st.markdown(f"<div style='text-align: center; font-size: 30px;'>📷</div>", 
                                   unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**{photo['desc']}**")
                        st.markdown(f"志愿者：{photo['volunteer']} | 服务：{photo['service']}")
                    st.markdown("---")
        
        with tab3:
            st.markdown("<h2 class='section-title'>上传新照片</h2>", 
                       unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("选择照片文件", 
                type=['jpg', 'jpeg', 'png', 'gif'],
                help="支持JPG、PNG、GIF格式，最大10MB")
            
            if uploaded_file is not None:
                # 显示预览
                col1, col2 = st.columns(2)
                with col1:
                    st.image(uploaded_file, caption="照片预览", use_column_width=True)
                
                with col2:
                    service_type = st.selectbox("关联服务", 
                        ["陪逛代购", "手机教学", "便民服务", "社区团购", "聊天陪伴", "医院陪诊"])
                    
                    photo_desc = st.text_area("照片描述", 
                        placeholder="描述这个温暖瞬间...",
                        height=100)
                    
                    share_option = st.radio("分享设置", 
                        ["仅自己可见", "分享给志愿者", "公开分享"])
                    
                    if st.button("保存到相册", use_container_width=True, type="primary"):
                        st.success("✅ 照片已保存到记忆相册！")
                        st.info("您可以在照片墙中查看这张照片")
    
    # ==================== 服务地图页面 ====================
    elif selected_page == "🗺️ 服务地图":
        st.markdown("<h1 class='main-title'>🗺️ 服务地图</h1>", unsafe_allow_html=True)
        
        # 地图功能
        st.markdown("<h2 class='section-title'>📍 附近服务分布</h2>", 
                   unsafe_allow_html=True)
        
        # 创建地图
        service_map = create_service_map()
        
        # 显示地图
        folium_static(service_map, width=1000, height=600)
        
        # 地图功能说明
        with st.expander("🗺️ 地图使用说明", expanded=True):
            st.markdown("""
            ### 地图图例说明
            - 🔵 **蓝色标记**：老人位置，需要服务
            - 🟢 **绿色标记**：志愿者位置，可提供服务
            - 🔴 **红色标记**：社区服务中心
            - 🟠 **橙色圆圈**：2公里服务范围
            
            ### 如何操作
            1. **缩放地图**：使用鼠标滚轮或地图控件
            2. **查看详情**：点击标记查看详细信息
            3. **移动地图**：按住鼠标左键拖动
            """)
        
        # 统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("附近老人", "8位", "+2")
        with col2:
            st.metric("可用志愿者", "5位", "在线")
        with col3:
            st.metric("平均距离", "1.2km", "较近")
        with col4:
            st.metric("服务覆盖率", "85%", "+5%")
        
        # 刷新地图按钮
        if st.button("🔄 刷新地图数据", use_container_width=True):
            st.rerun()
        
    # ==================== 数据看板页面 ====================
    elif selected_page == "📊 数据看板":
        st.markdown("<h1 class='main-title'>📊 运营数据全景看板</h1>", 
                   unsafe_allow_html=True)
    
        # 使用纯Streamlit版数据看板
        try:
            create_streamlit_dashboard()
        except Exception as e:
            st.error(f"数据看板加载出错: {str(e)}")
            
            # 备用方案：显示简单的指标
            st.markdown("### 📈 核心指标")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("累计订单", "1,568", "+12%")
            with col2:
                st.metric("活跃老人", "156", "+15")
            with col3:
                st.metric("志愿者数", "89", "+8")
            with col4:
                st.metric("满意度", "4.82", "+0.12")
    
        # 数据导出功能
        st.markdown("<h2 class='section-title'>📥 数据导出</h2>", 
                   unsafe_allow_html=True)
    
        export_col1, export_col2, export_col3 = st.columns(3)
        with export_col1:
            if st.button("📊 导出订单数据", use_container_width=True):
                csv = orders_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="下载CSV",
                    data=csv,
                    file_name="订单数据.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        with export_col2:
            if st.button("👥 导出志愿者数据", use_container_width=True):
                csv = volunteer_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="下载CSV",
                    data=csv,
                    file_name="志愿者数据.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        with export_col3:
            if st.button("📈 导出完整报告", use_container_width=True):
                st.success("完整报告已生成PDF文件")
    
    # ==================== 个人中心页面 ====================
    elif selected_page == "👤 个人中心":
        st.markdown(f"<h1 class='main-title'>👤 个人中心 - {st.session_state.username}</h1>", 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 我的资料", "📅 我的预约", "🎁 我的成就", "🔐 账户安全"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>个人信息</h2>", 
                       unsafe_allow_html=True)
            
            # 获取用户信息
            user_info = user_system.users.get(st.session_state.username, {})
            
            # 显示用户信息
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown("#### 基本信息")
                info_data = {
                    "用户名": st.session_state.username,
                    "用户类型": user_info.get('user_type', '用户'),
                    "身份": user_info.get('identity', '会员'),
                    "注册日期": user_info.get('reg_date', '2024-01-01'),
                    "年龄": user_info.get('age', '未设置'),
                    "手机号": user_info.get('phone', '未设置'),
                    "紧急联系人": user_info.get('emergency_contact', '未设置'),
                }
                
                for key, value in info_data.items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**{key}**")
                    with col2:
                        st.markdown(f"`{value}`")
            
            with info_col2:
                st.markdown("#### 服务与财务信息")
                service_data = {
                    "积分": user_info.get('points', 0),
                    "账户余额": f"¥{user_info.get('balance', 0):.2f}",
                    "累计消费": f"¥{user_info.get('total_spent', 0):.2f}",
                    "累计捐赠": f"¥{user_info.get('donation_total', 0):.2f}",
                    "服务次数": user_info.get('service_count', 0),
                    "累计时长": f"{user_info.get('total_hours', 0)}小时",
                    "当前评分": f"{user_info.get('rating', 0):.1f}/5.0",
                    "兴趣标签": ", ".join(user_info.get('interests', [])),
                    "个人简介": user_info.get('bio', '暂无简介'),
                }
                
                for key, value in service_data.items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**{key}**")
                    with col2:
                        if key == "兴趣标签" and not value:
                            st.markdown("`未设置`")
                        else:
                            st.markdown(f"`{value}`")
            
            st.markdown("---")
            st.markdown("<h3 class='section-title'>修改资料</h3>", 
                       unsafe_allow_html=True)
            
            edit_col1, edit_col2 = st.columns(2)
            with edit_col1:
                new_phone = st.text_input("新手机号", value=user_info.get('phone', ''))
                new_address = st.text_input("新地址", value=user_info.get('address', ''))
                emergency_contact = st.text_input("紧急联系人", value=user_info.get('emergency_contact', ''))
            with edit_col2:
                new_interests = st.multiselect("兴趣爱好", 
                    ["园艺", "书法", "戏曲", "烹饪", "散步", "聊天", "手工", "音乐", "运动", "阅读", "养生"],
                    default=user_info.get('interests', []))
                new_bio = st.text_area("个人简介", value=user_info.get('bio', ''), height=100)
            
            if st.button("更新资料", use_container_width=True, type="primary"):
                update_data = {
                    'phone': new_phone if new_phone else None,
                    'address': new_address if new_address else None,
                    'emergency_contact': emergency_contact if emergency_contact else None,
                    'interests': new_interests,
                    'bio': new_bio if new_bio else None
                }
                if user_system.update_profile(st.session_state.username, **update_data):
                    st.success("✅ 资料更新成功！")
                    st.rerun()
                else:
                    st.error("更新失败，请重试")
        
        with tab2:
            st.markdown("<h2 class='section-title'>我的预约记录</h2>", 
                       unsafe_allow_html=True)
            
            # 模拟预约记录
            appointments = [
                {"date": "2024-02-10", "service": "陪逛代购", "volunteer": "张明", 
                 "status": "已完成", "rating": 5.0, "amount": "60元"},
                {"date": "2024-02-08", "service": "手机教学", "volunteer": "李华", 
                 "status": "进行中", "rating": None, "amount": "50元"},
                {"date": "2024-02-05", "service": "聊天陪伴", "volunteer": "王芳", 
                 "status": "已完成", "rating": 4.8, "amount": "40元"},
                {"date": "2024-02-01", "service": "便民服务", "volunteer": "陈伟", 
                 "status": "已完成", "rating": 4.9, "amount": "30元"}
            ]
            
            for appt in appointments:
                with st.container():
                    cols = st.columns(6)
                    with cols[0]:
                        st.markdown(f"**{appt['date']}**")
                    with cols[1]:
                        st.markdown(f"🛠️ {appt['service']}")
                    with cols[2]:
                        st.markdown(f"👤 {appt['volunteer']}")
                    with cols[3]:
                        status_color = "#2ECC71" if appt['status'] == "已完成" else "#F39C12"
                        st.markdown(f"<span style='color:{status_color};'>● {appt['status']}</span>", 
                                   unsafe_allow_html=True)
                    with cols[4]:
                        st.markdown(f"💰 {appt['amount']}")
                    with cols[5]:
                        if appt['rating']:
                            st.markdown(f"⭐ {appt['rating']}")
                        else:
                            if st.button("评价", key=f"rate_{appt['date']}"):
                                st.success("跳转到评价页面")
                    st.markdown("---")
        
        with tab3:
            st.markdown("<h2 class='section-title'>我的成就勋章</h2>", 
                       unsafe_allow_html=True)
            
            achievements = [
                {"name": "初次见面", "desc": "完成第一次服务", "icon": "🎯", "unlocked": True},
                {"name": "忠实用户", "desc": "完成10次服务", "icon": "🏆", "unlocked": user_info.get('service_count', 0) >= 10},
                {"name": "社交达人", "desc": "与5位不同志愿者合作", "icon": "🤝", "unlocked": True},
                {"name": "学习之星", "desc": "完成手机教学课程", "icon": "📚", "unlocked": False},
                {"name": "社区之星", "desc": "参与社区活动", "icon": "🌟", "unlocked": False},
                {"name": "爱心天使", "desc": "累计捐赠50元", "icon": "❤️", "unlocked": user_info.get('donation_total', 0) >= 50},
                {"name": "VIP贵宾", "desc": "开通VIP会员", "icon": "👑", "unlocked": user_info.get('is_vip', False)},
                {"name": "积分达人", "desc": "获得1000积分", "icon": "⭐", "unlocked": user_info.get('points', 0) >= 1000}
            ]
            
            cols = st.columns(4)
            for idx, ach in enumerate(achievements):
                with cols[idx % 4]:
                    opacity = 1.0 if ach['unlocked'] else 0.3
                    st.markdown(f"""
                    <div style='
                        text-align: center;
                        opacity: {opacity};
                        padding: 15px;
                        background: {'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' if ach['unlocked'] else '#f8f9fa'};
                        border-radius: 10px;
                        margin: 10px 0;
                        border: 2px solid {'#FF8C00' if ach['unlocked'] else '#dee2e6'};
                    '>
                        <div style='font-size: 40px;'>{ach['icon']}</div>
                        <div style='font-weight: bold; font-size: 18px;'>{ach['name']}</div>
                        <div style='font-size: 14px; color: #666;'>{ach['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("<h2 class='section-title'>账户安全</h2>", 
                       unsafe_allow_html=True)
            
            security_col1, security_col2 = st.columns(2)
            with security_col1:
                st.markdown("#### 修改密码")
                current_pass = st.text_input("当前密码", type="password")
                new_pass = st.text_input("新密码", type="password")
                confirm_pass = st.text_input("确认新密码", type="password")
                
                if st.button("修改密码", use_container_width=True):
                    if not all([current_pass, new_pass, confirm_pass]):
                        st.error("请填写所有字段")
                    elif new_pass != confirm_pass:
                        st.error("两次输入的新密码不一致")
                    elif len(new_pass) < 6:
                        st.error("密码长度至少6位")
                    else:
                        # 验证当前密码
                        password_hash = hashlib.sha256(current_pass.encode()).hexdigest()
                        if user_info.get('password') == password_hash:
                            user_system.users[st.session_state.username]['password'] = hashlib.sha256(new_pass.encode()).hexdigest()
                            user_system.save_users()
                            st.success("✅ 密码修改成功！")
                        else:
                            st.error("当前密码错误")
            
            with security_col2:
                st.markdown("#### 安全设置")
                two_factor = st.checkbox("启用双重验证", value=False)
                login_notify = st.checkbox("登录通知", value=True)
                session_timeout = st.selectbox("会话超时", 
                    ["15分钟", "30分钟", "1小时", "4小时", "一天"])
                
                if st.button("保存安全设置", use_container_width=True):
                    st.success("✅ 安全设置已保存")
    
    # ==================== 系统设置页面 ====================
    elif selected_page == "⚙️ 系统设置":
        st.markdown("<h1 class='main-title'>⚙️ 系统设置</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔔 通知设置", "🎨 显示设置", "🔒 隐私设置"])
        
        with tab1:
            st.markdown("<h2 class='section-title'>通知偏好设置</h2>", 
                       unsafe_allow_html=True)
            
            notif_col1, notif_col2 = st.columns(2)
            with notif_col1:
                email_notif = st.checkbox("📧 邮箱通知", value=True)
                sms_notif = st.checkbox("📱 短信通知", value=True)
                app_notif = st.checkbox("📱 App推送", value=True)
            with notif_col2:
                remind_24h = st.checkbox("⏰ 提前24小时提醒", value=True)
                remind_1h = st.checkbox("⏰ 提前1小时提醒", value=True)
                feedback_notif = st.checkbox("💬 评价提醒", value=True)
            
            notification_frequency = st.select_slider("通知频率", 
                options=["实时", "每日一次", "每周一次", "仅重要通知"])
            
            if st.button("保存通知设置", use_container_width=True, type="primary"):
                st.success("✅ 通知设置已保存")
        
        with tab2:
            st.markdown("<h2 class='section-title'>显示与界面设置</h2>", 
                       unsafe_allow_html=True)
            
            display_col1, display_col2 = st.columns(2)
            with display_col1:
                font_size = st.select_slider("字体大小", 
                    options=["小", "中", "大", "特大"], value="大")
                
                color_mode = st.radio("颜色模式", 
                    ["明亮模式", "护眼模式", "深色模式"], horizontal=True)
                
                language = st.selectbox("界面语言", 
                    ["简体中文", "繁体中文", "English"])
            
            with display_col2:
                auto_play = st.checkbox("自动播放视频", value=False)
                show_images = st.checkbox("显示图片", value=True)
                simple_mode = st.checkbox("简洁模式", value=False)
            
            if st.button("保存显示设置", use_container_width=True, type="primary"):
                st.success("✅ 显示设置已保存")
        
        with tab3:
            st.markdown("<h2 class='section-title'>隐私设置</h2>", 
                       unsafe_allow_html=True)
            
            privacy_col1, privacy_col2 = st.columns(2)
            with privacy_col1:
                show_profile = st.radio("个人资料可见性", 
                    ["所有人可见", "仅志愿者可见", "仅自己可见"])
                show_location = st.checkbox("显示大致位置", value=True)
                allow_contact = st.checkbox("允许志愿者联系", value=True)
            
            with privacy_col2:
                data_sharing = st.checkbox("参与匿名数据统计", value=True)
                marketing_emails = st.checkbox("接收推广信息", value=False)
                third_party_share = st.checkbox("第三方数据共享", value=False)
            
            if st.button("保存隐私设置", use_container_width=True, type="primary"):
                st.success("✅ 隐私设置已保存")
    
    # ==================== 帮助页面 ====================
    else:
        st.markdown("<h1 class='main-title'>❓ 帮助与支持</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📖 使用指南", "❓ 常见问题", "📞 联系我们", "📝 反馈建议"])
        
        with tab1:
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
            - VIP会员享受专属折扣
            
            #### 3. 商业模式是什么？
            - 服务费收入（基础陪伴10元/小时）
            - 商家返佣（与商超、药店合作）
            - 增值服务（套餐、节日礼包）
            - 政府购买服务
            
            #### 4. 如何使用记忆相册？
            - 志愿者在服务后可上传照片
            - 您可以在"📸 记忆相册"中查看
            - 支持分享给家人朋友
            
            #### 5. 如何修改个人信息？
            - 进入"👤 个人中心"
            - 点击"修改资料"
            - 保存更改
            """)
        
        with tab2:
            faqs = {
                "Q1: 服务如何收费？": "A: 基础服务10元/小时，部分特殊服务可能额外收费。详细价格可在支付页面查看。",
                "Q2: VIP会员有什么优惠？": "A: VIP会员享受充值赠送、双倍积分、优先匹配、专属礼包等特权。",
                "Q3: 志愿者安全吗？": "A: 所有志愿者都经过实名认证和背景审核。",
                "Q4: 如何评价服务？": "A: 服务完成后可在个人中心进行评价。",
                "Q5: 可以指定志愿者吗？": "A: 可以，在智能匹配页面可以选择特定志愿者。",
                "Q6: 互助基金是什么？": "A: 每笔订单捐出0.5%给银龄互助基金，用于帮助特困老人。",
                "Q7: 忘记密码怎么办？": "A: 在登录页面点击'忘记密码'，通过手机验证重置。",
                "Q8: 如何联系客服？": "A: 可通过帮助页面的联系方式或在线客服联系。"
            }
            
            for question, answer in faqs.items():
                with st.expander(question):
                    st.write(answer)
        
        with tab3:
            st.markdown("""
            ### 📞 联系我们
            
            **客服热线：** 400-123-4567
            **服务时间：** 每天 8:00-22:00
            
            **邮箱：** support@yinlingdazi.com
            **微信：** 银龄搭子客服
            
            **办公地址：** 
            上海市徐汇区某某路123号
            银龄搭子服务中心
            
            **紧急联系：** 13142827079
            """)
            
            if st.button("在线客服", use_container_width=True):
                st.info("正在连接在线客服，请稍候...")
        
        with tab4:
            feedback_type = st.selectbox("反馈类型", 
                ["功能建议", "问题反馈", "投诉", "表扬", "其他"])
            
            feedback_content = st.text_area("反馈内容", 
                placeholder="请详细描述您的建议或问题...",
                height=150)
            
            contact_info = st.text_input("联系方式（选填）", 
                placeholder="邮箱/电话，便于我们回复您")
            
            if st.button("提交反馈", use_container_width=True, type="primary"):
                st.success("✅ 感谢您的反馈！")
                st.info("我们会在3个工作日内处理您的反馈。")

# ==================== 部署配置 ====================
if __name__ == "__main__":
    # 检查是否在云平台运行
    is_cloud = os.environ.get('STREAMLIT_SERVER_ADDRESS', '') != ''
    
    if is_cloud:
        st.info("🌐 运行在云平台，支持公网访问")
    
    # 运行主程序
    try:
        main()
    except Exception as e:
        st.error(f"程序运行出错: {str(e)}")
        st.info("请刷新页面重试，或联系技术支持")