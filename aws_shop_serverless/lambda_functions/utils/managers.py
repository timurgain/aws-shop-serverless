def join_product_stock(product, stocks):
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