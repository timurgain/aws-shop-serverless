def join_product_stock(product: dict, stocks: list) -> dict:
    return {
        **product,
        "count": next(
            (
                stock["count"]
                for stock in stocks
                if stock["product_id"] == product["id"]
            ),
            0,
        ),
    }