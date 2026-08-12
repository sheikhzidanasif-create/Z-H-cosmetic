import streamlit as st
import pandas as pd
from urllib.parse import quote
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Z&H Cosmetics",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Poppins:wght@300;400;500;600&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: #fffafa;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.brand {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    text-align: center;
}

.brand span {
    color: #b58a3a;
}

.subtitle {
    text-align: center;
    letter-spacing: 4px;
    font-size: 11px;
    color: #b58a3a;
}

.hero {
    padding: 70px 50px;
    border-radius: 20px;
    background: linear-gradient(
        120deg,
        #fff4f6,
        #f5dce2
    );
    margin-bottom: 40px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 65px;
    font-weight: 700;
    line-height: 1.05;
}

.hero-title span {
    color: #b58a3a;
}

.hero-text {
    color: #756b70;
    font-size: 17px;
    line-height: 1.8;
}

.product-card {
    background: white;
    border: 1px solid #f0e3e6;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 25px;
    min-height: 390px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.04);
}

.product-image {
    height: 190px;
    border-radius: 10px;
    background: linear-gradient(
        135deg,
        #f8e8ec,
        #ffffff
    );
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 70px;
}

.product-name {
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    margin-top: 15px;
}

.brand {
    color: #b58a3a;
    font-size: 12px;
    letter-spacing: 1px;
}

.price {
    font-weight: 600;
    font-size: 18px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
}

.dialog-box {
    padding: 40px;
    border-radius: 18px;
    background: linear-gradient(
        120deg,
        #ffffff,
        #f5dce2
    );
    margin: 40px 0;
}

.footer {
    margin-top: 50px;
    padding: 40px;
    background: #30242a;
    color: white;
    text-align: center;
}

div.stButton > button {
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# PRODUCT DATA
# =========================================================

products = [
    {
        "id": 1,
        "name": "Velvet Glow Foundation",
        "brand": "Z&H Beauty",
        "category": "Makeup",
        "price": 2499,
        "emoji": "💄"
    },
    {
        "id": 2,
        "name": "Rose Hydrating Serum",
        "brand": "Z&H Skin",
        "category": "Skincare",
        "price": 1999,
        "emoji": "🧴"
    },
    {
        "id": 3,
        "name": "Signature Rose Perfume",
        "brand": "Z&H Fragrance",
        "category": "Perfumes",
        "price": 3499,
        "emoji": "🌸"
    },
    {
        "id": 4,
        "name": "Silky Hair Serum",
        "brand": "Z&H Hair",
        "category": "Hair Care",
        "price": 1599,
        "emoji": "💇"
    },
    {
        "id": 5,
        "name": "Luxury Nail Polish",
        "brand": "Z&H Nails",
        "category": "Nail Products",
        "price": 899,
        "emoji": "💅"
    },
    {
        "id": 6,
        "name": "Soft Matte Lipstick",
        "brand": "Z&H Beauty",
        "category": "Makeup",
        "price": 1299,
        "emoji": "💋"
    },
    {
        "id": 7,
        "name": "Daily Glow Moisturizer",
        "brand": "Z&H Skin",
        "category": "Skincare",
        "price": 1799,
        "emoji": "✨"
    },
    {
        "id": 8,
        "name": "Bloom Body Mist",
        "brand": "Z&H Fragrance",
        "category": "Perfumes",
        "price": 2199,
        "emoji": "🌷"
    }
]

df = pd.DataFrame(products)


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "language" not in st.session_state:
    st.session_state.language = "English"


# =========================================================
# FUNCTIONS
# =========================================================

def money(price):
    return f"PKR {price:,}"


def add_to_cart(product_id):

    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1


def remove_from_cart(product_id):

    if product_id in st.session_state.cart:

        st.session_state.cart[product_id] -= 1

        if st.session_state.cart[product_id] <= 0:
            del st.session_state.cart[product_id]


def toggle_wishlist(product_id):

    if product_id in st.session_state.wishlist:

        st.session_state.wishlist.remove(product_id)

    else:

        st.session_state.wishlist.append(product_id)


def cart_total():

    total = 0

    for product_id, quantity in st.session_state.cart.items():

        product = df[df["id"] == product_id].iloc[0]

        total += product["price"] * quantity

    return total


def whatsapp_order():

    if not st.session_state.cart:
        return ""

    order_lines = []

    for product_id, quantity in st.session_state.cart.items():

        product = df[df["id"] == product_id].iloc[0]

        line = (
            f"{product['name']} "
            f"x{quantity} = "
            f"{money(product['price'] * quantity)}"
        )

        order_lines.append(line)

    order_text = "\n".join(order_lines)

    total = cart_total()

    message = f"""
Hello Z&H Cosmetics,

I want to place an order.

{order_text}

Total: {money(total)}

Delivery: Karachi

Please call me to confirm my order and delivery.
"""

    return (
        "https://wa.me/923089869634"
        "?text="
        + quote(message)
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand">
Z<span>&</span>H Cosmetics
</div>

<div class="subtitle">
LUXURY BEAUTY
</div>
""", unsafe_allow_html=True)


# =========================================================
# LANGUAGE
# =========================================================

col1, col2, col3 = st.columns([7, 1, 1])

with col2:

    if st.button("اردو"):

        st.session_state.language = "Urdu"


with col3:

    if st.button("EN"):

        st.session_state.language = "English"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🛍️ Z&H Cosmetics")

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Shop",
            "Cart",
            "Wishlist",
            "Beauty Dialog",
            "About",
            "Contact",
            "Admin"
        ]
    )


# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown("""
    <div class="hero">

        <div class="hero-title">
            Luxury Beauty,
            <br>
            <span>Made for You</span>
        </div>

        <p class="hero-text">
            Discover elegant makeup, skincare,
            perfumes, hair care and nail products.
        </p>

    </div>
    """, unsafe_allow_html=True)


    st.subheader("✨ Featured Products")

    featured = df.head(4)

    cols = st.columns(4)

    for col, (_, product) in zip(
        cols,
        featured.iterrows()
    ):

        with col:

            st.markdown(
                f"""
                <div class="product-card">

                    <div class="product-image">
                        {product['emoji']}
                    </div>

                    <div class="brand">
                        {product['brand']}
                    </div>

                    <div class="product-name">
                        {product['name']}
                    </div>

                    <div class="price">
                        {money(product['price'])}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Add to Cart",
                key=f"home_cart_{product['id']}"
            ):

                add_to_cart(product["id"])
                st.success("Added to cart!")


# =========================================================
# SHOP
# =========================================================

elif page == "Shop":

    st.markdown(
        '<div class="section-title">Shop</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        search = st.text_input(
            "🔎 Search Product"
        )


    with col2:

        category = st.selectbox(
            "Category",
            [
                "All",
                "Makeup",
                "Skincare",
                "Perfumes",
                "Hair Care",
                "Nail Products"
            ]
        )


    filtered = df.copy()


    if search:

        filtered = filtered[
            filtered["name"]
            .str.contains(
                search,
                case=False
            )
        ]


    if category != "All":

        filtered = filtered[
            filtered["category"] ==
            category
        ]


    st.write("")


    cols = st.columns(4)


    for index, (_, product) in enumerate(
        filtered.iterrows()
    ):

        with cols[index % 4]:

            st.markdown(
                f"""
                <div class="product-card">

                    <div class="product-image">
                        {product['emoji']}
                    </div>

                    <div class="brand">
                        {product['brand']}
                    </div>

                    <div class="product-name">
                        {product['name']}
                    </div>

                    <div class="price">
                        {money(product['price'])}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            c1, c2 = st.columns(2)


            with c1:

                if st.button(
                    "🛒 Add",
                    key=f"add_{product['id']}"
                ):

                    add_to_cart(
                        product["id"]
                    )

                    st.success(
                        "Added!"
                    )


            with c2:

                if st.button(
                    "❤️",
                    key=f"wish_{product['id']}"
                ):

                    toggle_wishlist(
                        product["id"]
                    )

                    st.success(
                        "Wishlist updated!"
                    )


# =========================================================
# CART
# =========================================================

elif page == "Cart":

    st.markdown(
        '<div class="section-title">🛒 Your Cart</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.cart:

        st.info(
            "Your cart is empty."
        )

    else:

        for product_id, quantity in list(
            st.session_state.cart.items()
        ):

            product = df[
                df["id"] == product_id
            ].iloc[0]


            col1, col2, col3, col4 = st.columns(
                [4, 1, 1, 2]
            )


            with col1:

                st.write(
                    f"**{product['name']}**"
                )


            with col2:

                st.write(
                    f"× {quantity}"
                )


            with col3:

                st.write(
                    money(
                        product["price"] *
                        quantity
                    )
                )


            with col4:

                if st.button(
                    "Remove",
                    key=f"remove_{product_id}"
                ):

                    remove_from_cart(
                        product_id
                    )

                    st.rerun()


        st.divider()


        st.subheader(
            f"Total: {money(cart_total())}"
        )


        st.info(
            "Delivery is available only in Karachi. "
            "Our delivery company will call to confirm "
            "and arrange parcel delivery."
        )


        whatsapp_url = whatsapp_order()


        if whatsapp_url:

            st.markdown(
                f"""
                <a href="{whatsapp_url}"
                target="_blank">

                <button style="
                    background:#25D366;
                    color:white;
                    padding:14px 25px;
                    border:none;
                    border-radius:7px;
                    font-size:16px;
                    cursor:pointer;
                ">
                📱 Order on WhatsApp
                </button>

                </a>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# WISHLIST
# =========================================================

elif page == "Wishlist":

    st.markdown(
        '<div class="section-title">❤️ Wishlist</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.wishlist:

        st.info(
            "Your wishlist is empty."
        )

    else:

        for product_id in st.session_state.wishlist:

            product = df[
                df["id"] == product_id
            ].iloc[0]


            st.write(
                f"### {product['emoji']} "
                f"{product['name']}"
            )

            st.write(
                money(product["price"])
            )


            if st.button(
                "Add to Cart",
                key=f"wishlist_cart_{product_id}"
            ):

                add_to_cart(product_id)

                st.success(
                    "Added to cart!"
                )


# =========================================================
# BEAUTY DIALOG
# =========================================================

elif page == "Beauty Dialog":

    st.markdown("""
    <div class="dialog-box">

        <div class="section-title">
            Beauty Dialog ✨
        </div>

        <p>
            Your Z&H beauty assistant.
        </p>

    </div>
    """, unsafe_allow_html=True)


    question = st.chat_input(
        "Ask about makeup, skincare, perfume..."
    )


    if question:

        st.chat_message(
            "user"
        ).write(question)


        text = question.lower()


        if "skin" in text:

            answer = """
            For skincare, a simple routine can include
            a gentle cleanser, moisturizer and sunscreen.
            You can also explore Z&H skincare products.
            """

        elif "perfume" in text:

            answer = """
            If you enjoy floral fragrances,
            you can explore our Signature Rose Perfume.
            """

        elif "makeup" in text:

            answer = """
            For makeup, you can explore foundation,
            lipstick, blush and other Z&H products.
            """

        elif "hair" in text:

            answer = """
            For hair care, explore shampoo,
            conditioner, hair oil and hair serum.
            """

        else:

            answer = """
            I can help with general beauty guidance
            and Z&H Cosmetics product suggestions.
            """


        st.chat_message(
            "assistant"
        ).write(answer)


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">About Z&H Cosmetics</div>',
        unsafe_allow_html=True
    )


    st.write("""
    Z&H Cosmetics is a premium beauty store offering
    products across:

    💄 Makeup

    🧴 Skincare

    🌸 Perfumes

    💇 Hair Care

    💅 Nail Products

    Our delivery service is available in Karachi.
    """)


# =========================================================
# CONTACT
# =========================================================

elif page == "Contact":

    st.markdown(
        '<div class="section-title">Contact Us</div>',
        unsafe_allow_html=True
    )


    st.write("""
    ### 📱 WhatsApp

    +92 308 9869634

    +92 315 8129255

    ### 📍 Delivery

    Karachi only.

    After placing an order, our delivery company
    will call you to confirm and arrange parcel delivery.
    """)


    st.markdown(
        """
        <a href="https://wa.me/923089869634"
        target="_blank">

        <button style="
            background:#25D366;
            color:white;
            border:none;
            padding:15px 25px;
            border-radius:7px;
            font-size:16px;
        ">
        💬 WhatsApp Z&H Cosmetics
        </button>

        </a>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ADMIN
# =========================================================

elif page == "Admin":

    st.markdown(
        '<div class="section-title">🔐 Admin Dashboard</div>',
        unsafe_allow_html=True
    )


    username = st.text_input(
        "Admin Username"
    )

    password = st.text_input(
        "Admin Password",
        type="password"
    )


    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.success(
                "Admin login successful!"
            )


            st.subheader(
                "Product Management"
            )


            product_name = st.text_input(
                "Product Name"
            )


            product_price = st.number_input(
                "Price PKR",
                min_value=0
            )


            product_category = st.selectbox(
                "Category",
                [
                    "Makeup",
                    "Skincare",
                    "Perfumes",
                    "Hair Care",
                    "Nail Products"
                ]
            )


            product_image = st.file_uploader(
                "Upload Product Image",
                type=[
                    "png",
                    "jpg",
                    "jpeg"
                ]
            )


            if st.button(
                "Add Product"
            ):

                st.success(
                    f"{product_name} "
                    "added successfully!"
                )


        else:

            st.error(
                "Invalid username or password."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <h2>
        Z&H Cosmetics
    </h2>

    <p>
        Luxury Beauty, Made for You
    </p>

    <p>
        Makeup • Skincare • Perfumes • Hair Care • Nails
    </p>

    <p>
        © 2026 Z&H Cosmetics
    </p>

</div>
""", unsafe_allow_html=True)
