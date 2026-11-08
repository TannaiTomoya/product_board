from app import Product, create_app, db

app = create_app()

# データベースを使う処理は、アプリの「中」（app_context）で実行する必要がある
with app.app_context():
    apple = Product(name="りんご（ふじ）", price=300, producer_name="高橋農園")
    db.session.add(apple)
    db.session.commit()
    print(f"登録しました: id={apple.id}")
