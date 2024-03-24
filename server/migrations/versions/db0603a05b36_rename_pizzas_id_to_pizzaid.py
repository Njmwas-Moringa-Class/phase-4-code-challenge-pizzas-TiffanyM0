"""rename pizzas_id to pizzaid

Revision ID: db0603a05b36
Revises: 0e677ac00567
Create Date: 2024-03-25 00:50:32.762170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0603a05b36'
down_revision = '0e677ac00567'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pizzas', schema=None) as batch_op:
        batch_op.drop_constraint('fk_pizzas_restaurant_id_restaurants', type_='foreignkey')
        batch_op.drop_column('restaurant_id')

    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('restaurant_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('pizza_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('fk_restaurant_pizzas_restaurants_id_restaurants', type_='foreignkey')
        batch_op.drop_constraint('fk_restaurant_pizzas_pizzas_id_pizzas', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), 'pizzas', ['pizza_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), 'restaurants', ['restaurant_id'], ['id'])
        batch_op.drop_column('pizzas_id')
        batch_op.drop_column('restaurants_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('restaurants_id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('pizzas_id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), type_='foreignkey')
        batch_op.create_foreign_key('fk_restaurant_pizzas_pizzas_id_pizzas', 'pizzas', ['pizzas_id'], ['id'])
        batch_op.create_foreign_key('fk_restaurant_pizzas_restaurants_id_restaurants', 'restaurants', ['restaurants_id'], ['id'])
        batch_op.drop_column('pizza_id')
        batch_op.drop_column('restaurant_id')

    with op.batch_alter_table('pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('restaurant_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_pizzas_restaurant_id_restaurants', 'restaurants', ['restaurant_id'], ['id'])

    # ### end Alembic commands ###