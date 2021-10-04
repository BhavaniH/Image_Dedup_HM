from sqlalchemy import Column, String, Integer,Table,MetaData,ForeignKey,BINARY,TEXT, BLOB, BIGINT, VARCHAR, LargeBinary
from sqlalchemy.orm import relationship, Session, sessionmaker,backref
from Database.base import engine


meta = MetaData()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


img_tags = Table(
    'img_tags', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('filename', String(20), unique=True),
    Column('block_1', String(125), nullable=True),
    Column('block_2', String(125), nullable=True),
    Column('block_3', String(125), nullable=True),
    Column('block_4', String(125), nullable=True),
    Column('block_5', String(125), nullable=True),
    Column('block_6', String(125), nullable=True),
    Column('block_7', String(125), nullable=True),
    Column('block_8', String(125), nullable=True),
    Column('block_9', String(125), nullable=True),
    Column('block_10', String(125), nullable=True),
    Column('block_11', String(125), nullable=True),
    Column('block_12', String(125), nullable=True),
    Column('block_13', String(125), nullable=True),
    Column('block_14', String(125), nullable=True),
    Column('block_15', String(125), nullable=True),
    Column('block_16', String(125), nullable=True),
)


img_keys = Table(
    'img_keys', meta,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('filename', String(20), unique=True),
    Column('block_1', BINARY(32), nullable=True),
    Column('block_2', BINARY(32), nullable=True),
    Column('block_3', BINARY(32), nullable=True),
    Column('block_4', BINARY(32), nullable=True),
    Column('block_5', BINARY(32), nullable=True),
    Column('block_6', BINARY(32), nullable=True),
    Column('block_7', BINARY(32), nullable=True),
    Column('block_8', BINARY(32), nullable=True),
    Column('block_9', BINARY(32), nullable=True),
    Column('block_10', BINARY(32), nullable=True),
    Column('block_11', BINARY(32), nullable=True),
    Column('block_12', BINARY(32), nullable=True),
    Column('block_13', BINARY(32), nullable=True),
    Column('block_14', BINARY(32), nullable=True),
    Column('block_15', BINARY(32), nullable=True),
    Column('block_16', BINARY(32), nullable=True),
)

img_users = Table(
    'img_users', meta,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('username', String(125), unique=True),
    Column('email', String(125), nullable=False),
    Column('password', String(125), nullable=False),
)


img_images = Table(
    'img_images', meta,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('imagename', String(125), unique=True),
    Column('image', LargeBinary),
)

img_cloud_cipher = Table(
    'img_cloud_cipher', meta,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('filename', String(20), unique=True),
    Column('block_1', TEXT, nullable=True),
    Column('block_2', TEXT, nullable=True),
    Column('block_3', TEXT, nullable=True),
    Column('block_4', TEXT, nullable=True),
    Column('block_5', TEXT, nullable=True),
    Column('block_6', TEXT, nullable=True),
    Column('block_7', TEXT, nullable=True),
    Column('block_8', TEXT, nullable=True),
    Column('block_9', TEXT, nullable=True),
    Column('block_10', TEXT, nullable=True),
    Column('block_11', TEXT, nullable=True),
    Column('block_12', TEXT, nullable=True),
    Column('block_13', TEXT, nullable=True),
    Column('block_14', TEXT, nullable=True),
    Column('block_15', TEXT, nullable=True),
    Column('block_16', TEXT, nullable=True),
)


img_cloud_tags = Table(
    'img_cloud_tags', meta,
    Column('id',Integer, primary_key=True,autoincrement=True),
    Column('filename', String(20), unique=True),
    Column('block_1', String(125), nullable=True),
    Column('block_2', String(125), nullable=True),
    Column('block_3', String(125), nullable=True),
    Column('block_4', String(125), nullable=True),
    Column('block_5', String(125), nullable=True),
    Column('block_6', String(125), nullable=True),
    Column('block_7', String(125), nullable=True),
    Column('block_8', String(125), nullable=True),
    Column('block_9', String(125), nullable=True),
    Column('block_10', String(125), nullable=True),
    Column('block_11', String(125), nullable=True),
    Column('block_12', String(125), nullable=True),
    Column('block_13', String(125), nullable=True),
    Column('block_14', String(125), nullable=True),
    Column('block_15', String(125), nullable=True),
    Column('block_16', String(125), nullable=True),
    #relationship("img_cloud_cipher", backref=backref("img_cloud_tags", uselist=False)),
)

img_enc_tags = Table(
    'img_enc_tags', meta,
    Column('id',Integer, primary_key=True,autoincrement=True),
    Column('filename', String(20), unique=True),
    Column('block_1', String(125), nullable=True),
    Column('block_2', String(125), nullable=True),
    Column('block_3', String(125), nullable=True),
    Column('block_4', String(125), nullable=True),
    Column('block_5', String(125), nullable=True),
    Column('block_6', String(125), nullable=True),
    Column('block_7', String(125), nullable=True),
    Column('block_8', String(125), nullable=True),
    Column('block_9', String(125), nullable=True),
    Column('block_10', String(125), nullable=True),
    Column('block_11', String(125), nullable=True),
    Column('block_12', String(125), nullable=True),
    Column('block_13', String(125), nullable=True),
    Column('block_14', String(125), nullable=True),
    Column('block_15', String(125), nullable=True),
    Column('block_16', String(125), nullable=True),
)
meta.create_all(engine)