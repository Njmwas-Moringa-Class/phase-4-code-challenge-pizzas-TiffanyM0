"""update relationships

Revision ID: cbaf0992e349
Revises: 32badea0c9cb
Create Date: 2024-03-24 22:44:00.343139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbaf0992e349'
down_revision = '32badea0c9cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurant_pizza')
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pizzas_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('restaurants_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_pizzas_id_pizzas'), 'pizzas', ['pizzas_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_restaurants_id_restaurants'), 'restaurants', ['restaurants_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_restaurants_id_restaurants'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_pizzas_id_pizzas'), type_='foreignkey')
        batch_op.drop_column('restaurants_id')
        batch_op.drop_column('pizzas_id')

    op.create_table('restaurant_pizza',
    sa.Column('pizzas_id', sa.INTEGER(), nullable=True),
    sa.Column('restaurant_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['pizzas_id'], ['pizzas.id'], name='fk_restaurant_pizza_pizzas_id_pizzas'),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], name='fk_restaurant_pizza_restaurant_id_restaurants')
    )
    # ### end Alembic commands ###