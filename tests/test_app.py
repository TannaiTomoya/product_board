from app import Product, db, validate_product


def add_product(app, **kwargs):
    """テスト用に商品を1件登録して、その id を返す"""
    values = {"name": "りんご", "price": 300, "producer_name": "高橋農園"}
    values.update(kwargs)
    with app.app_context():
        product = Product(**values)
        db.session.add(product)
        db.session.commit()
        return product.id


# --- 入力チェック ---


def test_validate_product_ok():
    form = {"name": "りんご", "price": "300", "producer_name": "高橋農園"}
    assert validate_product(form) == []


def test_validate_product_empty():
    errors = validate_product({"name": "", "price": "", "producer_name": ""})
    assert "商品名を入力してください" in errors
    assert "価格は0以上の整数で入力してください" in errors
    assert "生産者名を入力してください" in errors


def test_validate_product_too_long_name_and_high_price():
    form = {"name": "あ" * 51, "price": "100001", "producer_name": "高橋農園"}
    errors = validate_product(form)
    assert "商品名は50文字以内で入力してください" in errors
    assert "価格は100,000円以下で入力してください" in errors


# --- 各ページ ---


def test_index_empty(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "まだ商品がありません。" in response.text


def test_create_product(client, app):
    response = client.post(
        "/products/new",
        data={"name": "りんご", "price": "300", "producer_name": "高橋農園"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "商品を登録しました" in response.text
    assert "りんご" in response.text
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count(Product.id))) == 1


def test_create_product_invalid(client, app):
    response = client.post(
        "/products/new", data={"name": "", "price": "-1", "producer_name": ""}
    )
    assert response.status_code == 422
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count(Product.id))) == 0


def test_show_product(client, app):
    product_id = add_product(app)
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert "りんご" in response.text


def test_show_missing_product_is_404(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "ページが見つかりません" in response.text


def test_edit_product(client, app):
    product_id = add_product(app)
    response = client.post(
        f"/products/{product_id}/edit",
        data={"name": "みかん", "price": "500", "producer_name": "佐藤農園"},
        follow_redirects=True,
    )
    assert "商品を更新しました" in response.text
    with app.app_context():
        product = db.session.get(Product, product_id)
        assert product.name == "みかん"
        assert product.price == 500


def test_delete_product(client, app):
    product_id = add_product(app)
    response = client.post(f"/products/{product_id}/delete", follow_redirects=True)
    assert "商品を削除しました" in response.text
    with app.app_context():
        assert db.session.get(Product, product_id) is None
