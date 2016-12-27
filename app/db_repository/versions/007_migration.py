from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
person = Table('person', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('number', VARCHAR(length=120)),
    Column('awards_given_id', INTEGER),
    Column('awards_gotten_id', INTEGER),
    Column('total_points', FLOAT),
)

person = Table('person', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('number', String(length=120)),
    Column('total_points', Float),
    Column('given_id', Integer),
    Column('gotten_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['awards_given_id'].drop()
    pre_meta.tables['person'].columns['awards_gotten_id'].drop()
    post_meta.tables['person'].columns['given_id'].create()
    post_meta.tables['person'].columns['gotten_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['awards_given_id'].create()
    pre_meta.tables['person'].columns['awards_gotten_id'].create()
    post_meta.tables['person'].columns['given_id'].drop()
    post_meta.tables['person'].columns['gotten_id'].drop()
