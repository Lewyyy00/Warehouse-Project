"""transfered cloumn quantity to Product

Revision ID: 852472e79167
Revises: 085ec8327a72
Create Date: 2024-12-16 16:26:07.666069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '852472e79167'
down_revision = '085ec8327a72'
branch_labels = None
depends_on = None


def upgrade():
    # Dodanie kolumny z wartością domyślną
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False, server_default="0"))

    # Usunięcie kolumny `quantity` z tabeli `user_products`
    with op.batch_alter_table('user_products', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # Usunięcie kolumny `created_at` z tabeli `users`
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')


def downgrade():
    # Przywrócenie kolumny `created_at` w tabeli `users`
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))

    # Przywrócenie kolumny `quantity` w tabeli `user_products`
    with op.batch_alter_table('user_products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.INTEGER(), nullable=False))

    # Usunięcie kolumny `quantity` z tabeli `products`
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('quantity')
