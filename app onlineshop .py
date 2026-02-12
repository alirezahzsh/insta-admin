import streamlit as st
import pandas as pd

# تنظیمات صفحه برای نمایش بهتر در موبایل ادمین‌ها
st.set_page_config(page_title="Insta-Admin VIP", page_icon="🚀", layout="centered")

# --- مدیریت حافظه (دیتابیس موقت) ---
# در نسخه پیشرفته، این بخش به دیتابیس واقعی وصل می‌شود
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame([
        {'نام محصول': 'مانتو کتی', 'قیمت': 580000, 'موجودی': 10},
        {'نام محصول': 'شلوار جین', 'قیمت': 450000, 'موجودی': 5}
    ])

if 'card_number' not in st.session_state:
    st.session_state.card_number = "۶۰۳۷-۹۹۷۱-۰۰۰۰-۰۰۰۰"

# --- منوی ناوبری ---
menu = st.sidebar.radio("منوی مدیریت", ["📝 صدور فاکتور", "⚙️ تنظیمات پنل شما"])

# --- بخش تنظیمات (جایی که مشتری خودش دیتایش را وارد می‌کند) ---
if menu == "⚙️ تنظیمات پنل شما":
    st.header("⚙️ شخصی‌سازی پنل فروشگاه")
    
    # تنظیم شماره کارت
    st.session_state.card_number = st.text_input("شماره کارت جهت درج در فاکتور:", st.session_state.card_number)
    
    st.subheader("📦 مدیریت لیست محصولات")
    # ویرایش مستقیم محصولات توسط مشتری
    edited_df = st.data_editor(st.session_state.products, num_rows="dynamic", use_container_width=True)
    if st.button("💾 ذخیره تغییرات انبار"):
        st.session_state.products = edited_df
        st.success("لیست محصولات با موفقیت آپدیت شد!")

# --- بخش صدور فاکتور (بخش اصلی کار ادمین) ---
else:
    st.header("📝 صدور فاکتور سریع")
    
    if st.session_state.products.empty:
        st.warning("ابتدا از بخش تنظیمات، محصولات خود را وارد کنید.")
    else:
        # انتخاب محصول از لیستی که مشتری خودش ساخته
        product_names = st.session_state.products['نام محصول'].tolist()
        selected_p = st.selectbox("انتخاب محصول:", product_names)
        
        # استخراج قیمت
        p_info = st.session_state.products[st.session_state.products['نام محصول'] == selected_p].iloc[0]
        
        customer = st.text_input("نام مشتری:")
        
        if st.button("🚀 ساخت متن فاکتور"):
            total_price = p_info['قیمت'] + 30000 # هزینه پست فرضی
            
            factor_body = f"""
            🌸 سلام {customer} عزیز، فاکتور خدمت شما:
            
            🛍️ محصول: {selected_p}
            💰 مبلغ کل: {total_price:,.0f} تومان
            💳 شماره کارت: {st.session_state.card_number}
            
            🙏 لطفاً پس از واریز، تصویر فیش را بفرستید.
            """
            st.text_area("کپی و ارسال در دایرکت:", factor_body, height=200)
            st.info("💡 این متن را کپی کرده و برای مشتری بفرستید.")

# --- فوتر برای فروش به مشتری ---
st.sidebar.markdown("---")
st.sidebar.write("💎 نسخه VIP فعال است")
