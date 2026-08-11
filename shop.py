from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from extensions import db
from models import Redemption

SHOP_ITEMS = [
    {
        'slug': 'wallpaper-pack',
        'name': 'Wallpaper Pack',
        'description': 'A set of desktop & phone wallpapers from the gallery.',
        'emoji': '🖼',
        'cost': 15,
        'category': 'Digital',
    },
    {
        'slug': 'sticker-pack',
        'name': 'Sticker Pack',
        'description': 'A digital sticker pack, ready for Discord or wherever.',
        'emoji': '✨',
        'cost': 20,
        'category': 'Digital',
    },
    {
        'slug': 'credits-listing',
        'name': 'Name in Credits',
        'description': 'Your name added to the supporters/credits page.',
        'emoji': '📜',
        'cost': 10,
        'category': 'Flair',
    },
    {
        'slug': 'profile-badge',
        'name': 'Custom Profile Badge',
        'description': 'A one-of-a-kind badge on your community profile.',
        'emoji': '🎖',
        'cost': 40,
        'category': 'Flair',
    },
    {
        'slug': 'custom-emoji',
        'name': 'Custom Emoji Request',
        'description': 'A custom emoji made just for you.',
        'emoji': '🐾',
        'cost': 60,
        'category': 'Commissions',
    },
    {
        'slug': 'doodle-request',
        'name': '1:1 Doodle Request',
        'description': 'A small personalized doodle, just for you.',
        'emoji': '🖌',
        'cost': 150,
        'category': 'Commissions',
    },
]

SHOP_ITEMS_BY_SLUG = {item['slug']: item for item in SHOP_ITEMS}


def register_shop_routes(app):
    @app.route('/shop')
    def shop():
        return render_template('shop.html', title="Shop", items=SHOP_ITEMS)

    @app.route('/redeem', methods=['POST'])
    @login_required
    def redeem():
        data = request.get_json(silent=True) or {}
        item = SHOP_ITEMS_BY_SLUG.get(data.get('slug'))
        if not item:
            return jsonify({'error': 'Item not found.'}), 404

        if current_user.stardust_balance < item['cost']:
            return jsonify({'error': 'Not enough stardust.'}), 400

        current_user.stardust_balance -= item['cost']
        db.session.add(Redemption(
            user_id=current_user.id,
            item_slug=item['slug'],
            item_name=item['name'],
            cost=item['cost'],
            status='pending',
        ))
        db.session.commit()
        return jsonify({'balance': current_user.stardust_balance})
