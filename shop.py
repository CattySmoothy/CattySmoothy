import random

from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from extensions import db
from models import Redemption, WishPull, User

SHOP_ITEMS = [
    {
        'slug': 'wallpaper-pack',
        'name': 'Wallpaper Pack',
        'description': 'A set of desktop & phone wallpapers from the gallery.',
        'icon': 'frame',
        'cost': 15,
        'category': 'Digital',
    },
    {
        'slug': 'sticker-pack',
        'name': 'Sticker Pack',
        'description': 'A digital sticker pack, ready for Discord or wherever.',
        'icon': 'sparkle',
        'cost': 20,
        'category': 'Digital',
    },
    {
        'slug': 'credits-listing',
        'name': 'Name in Credits',
        'description': 'Your name added to the supporters/credits page.',
        'icon': 'scroll',
        'cost': 10,
        'category': 'Flair',
    },
    {
        'slug': 'profile-badge',
        'name': 'Custom Profile Badge',
        'description': 'A one-of-a-kind badge on your community profile.',
        'icon': 'medal',
        'cost': 40,
        'category': 'Flair',
    },
    {
        'slug': 'custom-emoji',
        'name': 'Custom Emoji Request',
        'description': 'A custom emoji made just for you.',
        'icon': 'paw',
        'cost': 60,
        'category': 'Commissions',
    },
    {
        'slug': 'doodle-request',
        'name': '1:1 Doodle Request',
        'description': 'A small personalized doodle, just for you.',
        'icon': 'brush',
        'cost': 150,
        'category': 'Commissions',
    },
]

SHOP_ITEMS_BY_SLUG = {item['slug']: item for item in SHOP_ITEMS}

# ── Wish (gacha-style pull) ──────────────────────────────────────────────
# Weights sum to 100 → roughly 75% common / 20% rare / 5% legendary, the
# same shape most gacha banners use. Rare/legendary wins hand over a real
# shop item for free instead of stardust.
WISH_COST = 10
WISH_POOL = [
    {'label': '2 Stardust',           'rarity': 'common',    'weight': 30, 'reward_type': 'stardust', 'reward_value': '2'},
    {'label': '3 Stardust',           'rarity': 'common',    'weight': 25, 'reward_type': 'stardust', 'reward_value': '3'},
    {'label': '5 Stardust',           'rarity': 'common',    'weight': 20, 'reward_type': 'stardust', 'reward_value': '5'},
    {'label': '15 Stardust',          'rarity': 'rare',      'weight': 8,  'reward_type': 'stardust', 'reward_value': '15'},
    {'label': 'Name in Credits',      'rarity': 'rare',      'weight': 12, 'reward_type': 'item',     'reward_value': 'credits-listing'},
    {'label': 'Custom Profile Badge', 'rarity': 'legendary', 'weight': 4,  'reward_type': 'item',     'reward_value': 'profile-badge'},
    {'label': 'Custom Emoji Request', 'rarity': 'legendary', 'weight': 1,  'reward_type': 'item',     'reward_value': 'custom-emoji'},
]


def _pick_wish_reward():
    total = sum(e['weight'] for e in WISH_POOL)
    roll = random.uniform(0, total)
    upto = 0
    for entry in WISH_POOL:
        upto += entry['weight']
        if roll <= upto:
            return entry
    return WISH_POOL[-1]


def register_shop_routes(app):
    @app.route('/shop')
    def shop():
        recent_wishes = []
        if current_user.is_authenticated:
            pulls = (WishPull.query.filter_by(user_id=current_user.id)
                     .order_by(WishPull.created_at.desc()).limit(8).all())
            recent_wishes = [p.to_dict() for p in pulls]
        return render_template('shop.html', title="Shop", items=SHOP_ITEMS,
                               wish_cost=WISH_COST, recent_wishes=recent_wishes)

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

    @app.route('/shop/gift', methods=['POST'])
    @login_required
    def gift_item():
        data = request.get_json(silent=True) or {}
        item = SHOP_ITEMS_BY_SLUG.get(data.get('slug'))
        if not item:
            return jsonify({'error': 'Item not found.'}), 404

        recipient_email = (data.get('email') or '').strip().lower()
        if not recipient_email:
            return jsonify({'error': "Enter the recipient's email."}), 400

        recipient = User.query.filter_by(email=recipient_email).first()
        if not recipient:
            return jsonify({'error': 'No account with that email.'}), 404
        if recipient.id == current_user.id:
            return jsonify({'error': "That's you — just redeem it instead."}), 400
        if current_user.stardust_balance < item['cost']:
            return jsonify({'error': 'Not enough stardust.'}), 400

        current_user.stardust_balance -= item['cost']
        db.session.add(Redemption(
            user_id=recipient.id,
            item_slug=item['slug'],
            item_name=item['name'],
            cost=item['cost'],
            status='pending',
            gifted_by_id=current_user.id,
        ))
        db.session.commit()
        recipient_name = recipient.email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
        return jsonify({'balance': current_user.stardust_balance, 'recipient_name': recipient_name})

    @app.route('/shop/wish', methods=['POST'])
    @login_required
    def wish():
        if current_user.stardust_balance < WISH_COST:
            return jsonify({'error': 'Not enough stardust for a Wish.'}), 400

        current_user.stardust_balance -= WISH_COST
        reward = _pick_wish_reward()

        if reward['reward_type'] == 'stardust':
            current_user.stardust_balance += int(reward['reward_value'])
        else:
            item = SHOP_ITEMS_BY_SLUG.get(reward['reward_value'])
            if item:
                db.session.add(Redemption(
                    user_id=current_user.id,
                    item_slug=item['slug'],
                    item_name=item['name'],
                    cost=0,
                    status='pending',
                    note='a Wish reward',
                ))

        db.session.add(WishPull(
            user_id=current_user.id,
            rarity=reward['rarity'],
            label=reward['label'],
            reward_type=reward['reward_type'],
            reward_value=reward['reward_value'],
        ))
        db.session.commit()
        return jsonify({
            'balance': current_user.stardust_balance,
            'reward': {'label': reward['label'], 'rarity': reward['rarity']},
        })
