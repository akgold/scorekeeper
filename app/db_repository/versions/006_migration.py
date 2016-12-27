from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
award = Table('award', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('amount', INTEGER),
    Column('reason', TEXT),
    Column('time', DATETIME),
    Column('to_id', INTEGER),
    Column('from_id', INTEGER),
)

award = Table('award', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('amount', Integer),
    Column('reason', Text),
    Column('time', DateTime),
    Column('giver_id', Integer),
    Column('getter_id', Integer),
)

person = Table('person', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('number', String(length=120)),
    Column('total_points', Float),
    Column('awards_given_id', Integer),
    Column('awards_gotten_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['award'].columns['from_id'].drop()
    pre_meta.tables['award'].columns['to_id'].drop()
    post_meta.tables['award'].columns['getter_id'].create()
    post_meta.tables['award'].columns['giver_id'].create()
    post_meta.tables['person'].columns['awards_given_id'].create()
    post_meta.tables['person'].columns['awards_gotten_id'].create()
    post_meta.tables['person'].columns['total_points'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['award'].columns['from_id'].create()
    pre_meta.tables['award'].columns['to_id'].create()
    post_meta.tables['award'].columns['getter_id'].drop()
    post_meta.tables['award'].columns['giver_id'].drop()
    post_meta.tables['person'].columns['awards_given_id'].drop()
    post_meta.tables['person'].columns['awards_gotten_id'].drop()
    post_meta.tables['person'].columns['total_points'].drop()
