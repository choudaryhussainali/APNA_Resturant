import streamlit as st
import datetime

# Expanded Menu
menu = {
    "Starters": {"Soup": 250, "Fries": 200, "Spring Rolls": 350},
    "Main Course": {"Pizza": 2000, "Burger": 400, "Pasta": 1000, "Biryani": 500},
    "Fast Food": {"Shawarma": 400, "Sandwich": 250, "Tacos": 350},
    "Drinks": {"Coke": 150, "Fresh Juice": 250, "Coffee": 200},
    "Desserts": {"Ice Cream": 300, "Cake Slice": 350, "Donut": 150}
}

st.set_page_config(page_title="🍴 APNA RESTAURANT POS", layout="wide")
st.title("🍽️ APNA RESTAURANT - Self Ordering System")
st.write("Welcome! Please select your items below 👇")

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "invoice_lines" not in st.session_state:
    st.session_state.invoice_lines = None
if "final_total" not in st.session_state:
    st.session_state.final_total = 0

# ----------------- 🍲 Menu Display -----------------
for category, items in menu.items():
    st.subheader(category)
    cols = st.columns(len(items))
    for i, (item, price) in enumerate(items.items()):
        qty = cols[i].number_input(
            f"{item} (Rs {price})",
            min_value=0,
            max_value=20,
            step=1,
            key=f"qty_{item}"
        )
        if qty > 0:
            st.session_state.cart[item] = {"price": price, "qty": qty}
        elif item in st.session_state.cart:
            del st.session_state.cart[item]

# ----------------- 🧾 Checkout -----------------
if st.button("🧾 Generate Bill"):
    if st.session_state.cart:
        total = 0
        invoice_lines = []
        invoice_lines.append("======= APNA RESTAURANT INVOICE =======")
        invoice_lines.append(f"Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        invoice_lines.append("---------------------------------------")

        for item, details in st.session_state.cart.items():
            cost = details["price"] * details["qty"]
            total += cost
            invoice_lines.append(f"{item} x {details['qty']} = Rs {cost}")

        invoice_lines.append("---------------------------------------")
        invoice_lines.append(f"Total Bill: Rs {total}")

        # Discount
        if total > 1000:
            discount = total * 0.1
            final_total = total - discount
            invoice_lines.append(f"Discount Applied (10%): Rs {discount}")
        else:
            final_total = total
            invoice_lines.append("No discount applied.")

        invoice_lines.append(f"Final Amount: Rs {final_total}")
        invoice_lines.append("======== THANK YOU, VISIT AGAIN ========")

        # Save to session_state
        st.session_state.invoice_lines = invoice_lines
        st.session_state.final_total = final_total

        # Save invoice to file
        with open("orders.txt", "a") as f:
            f.write("\n".join(invoice_lines))
            f.write("\n\n")
    else:
        st.error("⚠️ Your cart is empty. Please add items first.")

# ----------------- 📄 Show Invoice -----------------
if st.session_state.invoice_lines:
    st.subheader("=== Invoice ===")
    for line in st.session_state.invoice_lines:
        st.write(line)

    # Download option
    st.download_button(
        label="📥 Download Invoice",
        data="\n".join(st.session_state.invoice_lines),
        file_name=f"invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

    # Payment options
    payment = st.radio("💳 Select Payment Method:", ["Cash", "Card", "Digital Wallet"])
    if st.button("✅ Confirm Payment"):
        st.success(f"Payment successful via {payment}! ✅")
