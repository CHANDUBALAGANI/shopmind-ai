import os
from groq import Groq

from products.models import Product


def get_product_context():
    """
    Get available products from the database
    and prepare them for the AI assistant.
    """

    products = Product.objects.select_related("category").filter(
        stock__gt=0
    )

    product_data = []

    for product in products:
        product_data.append({
            "id": product.id,
            "name": product.name,
            "category": product.category.name,
            "price": float(product.price),
            "description": product.description,
            "stock": product.stock,
        })

    return product_data


def get_product_context_text():
    """
    Convert product information into text
    that can be provided to the AI.
    """

    products = get_product_context()

    if not products:
        return "No products are currently available."

    lines = []

    for product in products:
        lines.append(
            f"""
Product ID: {product['id']}
Name: {product['name']}
Category: {product['category']}
Price: ₹{product['price']:,.2f}
Stock: {product['stock']}
Description: {product['description']}
"""
        )

    return "\n".join(lines)


def ask_shopmind_ai(user_message):
    """
    Send the user's question and product information
    to the ShopMind AI assistant.
    """

    product_context = get_product_context_text()

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = f"""
You are ShopMind AI, a helpful shopping assistant for an
e-commerce website.

Your job is to help customers choose products from the
products available in the ShopMind store.

IMPORTANT RULES:

1. Recommend products only from the products provided below.
2. Never invent a product that is not provided.
3. Never invent a price or stock quantity.
4. If a suitable product is not available, say so clearly.
5. Keep responses concise and easy to understand.
6. When recommending a product, mention its name and price.
7. Respect the customer's budget.
8. Use the product category when relevant.
9. Compare products only using the information provided.
10. Do not claim that you placed an order or completed a purchase.

AVAILABLE SHOPMIND PRODUCTS:

{product_context}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content