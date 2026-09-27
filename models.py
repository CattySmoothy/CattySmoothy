from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

# The one account allowed to see/manage the commission queue (models.py, not
# a role column, since there is exactly one artist running this site).
OWNER_EMAIL = 'raichuuxxofficial@gmail.com'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    stardust_balance = db.Column(db.Integer, default=0, nullable=False)
    login_streak = db.Column(db.Integer, default=0, nullable=False)
    longest_login_streak = db.Column(db.Integer, default=0, nullable=False)
    last_login_date = db.Column(db.Date, nullable=True)

    purchases = db.relationship('Purchase', backref='user', lazy='dynamic')
    redemptions = db.relationship('Redemption', foreign_keys='Redemption.user_id', backref='user', lazy='dynamic')
    guestbook_entries = db.relationship('GuestbookEntry', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def record_visit(self):
        """Update the login streak for today's visit. Safe to call on every
        request while authenticated — a no-op if already recorded today."""
        today = datetime.utcnow().date()
        if self.last_login_date == today:
            return
        if self.last_login_date is not None and (today - self.last_login_date).days == 1:
            self.login_streak += 1
        else:
            self.login_streak = 1
        self.longest_login_streak = max(self.longest_login_streak, self.login_streak)
        self.last_login_date = today

    @property
    def active_membership(self):
        return (self.purchases
                .filter_by(type='membership', status='completed')
                .order_by(Purchase.created_at.desc())
                .first())


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    stripe_session_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(20), nullable=False)  # 'donation' | 'membership'
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending|completed|refunded|canceled
    plan_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Redemption(db.Model):
    __tablename__ = 'redemptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    item_slug = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending|fulfilled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # set when this redemption was a gift — the sender paid the cost, this
    # row belongs to the recipient (user_id above)
    gifted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    note = db.Column(db.String(200), nullable=True)  # e.g. "a Wish reward" or a gift message

    gifted_by = db.relationship('User', foreign_keys=[gifted_by_id])


class WishPull(db.Model):
    """One pull from the Shop's Wish (gacha) banner."""
    __tablename__ = 'wish_pulls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rarity = db.Column(db.String(20), nullable=False)  # common | rare | legendary
    label = db.Column(db.String(100), nullable=False)
    reward_type = db.Column(db.String(20), nullable=False)  # stardust | item
    reward_value = db.Column(db.String(50), nullable=False)  # amount, or an item slug
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'rarity': self.rarity,
            'label': self.label,
            'created_at': self.created_at.strftime('%b %d, %Y'),
        }


class Commission(db.Model):
    """A single commission moving through the queue — client, price and
    deadline, plus a checklist of production tasks."""
    __tablename__ = 'commissions'

    STATUSES = ('queued', 'in_progress', 'review', 'done')

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(8, 2), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='queued', index=True)
    deadline = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = db.relationship(
        'CommissionTask', backref='commission', lazy='dynamic',
        order_by='CommissionTask.position', cascade='all, delete-orphan',
    )

    def to_dict(self):
        tasks = self.tasks.all()
        return {
            'id': self.id,
            'client_name': self.client_name,
            'title': self.title,
            'description': self.description or '',
            'price': float(self.price) if self.price is not None else None,
            'status': self.status,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'notes': self.notes or '',
            'position': self.position,
            'tasks': [t.to_dict() for t in tasks],
            'task_total': len(tasks),
            'task_done': sum(1 for t in tasks if t.done),
        }


class CommissionTask(db.Model):
    """One checklist item on a commission (e.g. "sketch", "lineart")."""
    __tablename__ = 'commission_tasks'

    id = db.Column(db.Integer, primary_key=True)
    commission_id = db.Column(db.Integer, db.ForeignKey('commissions.id'), nullable=False, index=True)
    label = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'label': self.label, 'done': self.done}


class EarningsGoal(db.Model):
    """A single row: the artist's current earnings target for the queue's
    progress bar. Always read/written as 'the latest row' rather than a
    fixed id, so updating it is a plain insert-and-move-on."""
    __tablename__ = 'earnings_goals'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Question(db.Model):
    """A comment/question posted from the Support page's comment section.
    Signed-in visitors only — the poster is a real account, not a typed-in
    name, so there's no name/email fields to fill in or fake."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    answered = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = db.relationship('User')

    def to_dict(self):
        # Never expose the poster's email — just a display name, the same
        # way the home page turns an account into one.
        name = 'Someone'
        if self.user:
            name = self.user.email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
        return {
            'id': self.id,
            'name': name,
            'message': self.message,
            'answered': self.answered,
            'created_at': self.created_at.strftime('%b %d, %Y'),
        }


class GuestbookEntry(db.Model):
    __tablename__ = 'guestbook_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    display_name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
