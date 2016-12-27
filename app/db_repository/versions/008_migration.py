from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
person = Table('person', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('number', VARCHAR(length=120)),
    Column('total_points', FLOAT),
    Column('given_id', INTEGER),
    Column('gotten_id', INTEGER),
)

award = Table('award', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('amount', INTEGER),
    Column('reason', TEXT),
    Column('time', DATETIME),
    Column('getter_id', INTEGER),
    Column('giver_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['given_id'].drop()
    pre_meta.tables['person'].columns['gotten_id'].drop()
    pre_meta.tables['award'].columns['giver_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['given_id'].create()
    pre_meta.tables['person'].columns['gotten_id'].create()
    pre_meta.tables['award'].columns['giver_id'].create()
