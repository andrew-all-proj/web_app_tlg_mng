import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE)  # , echo=True

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    id_telegram = Column(Integer, nullable=False, unique=True)
    date_regestration = Column(DateTime, nullable=False, default=datetime.datetime.now)
    data_update = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    role = Column(Boolean, nullable=False, default=False)
    is_archive = Column(Boolean, nullable=False, default=False)
    media = relationship("MediaContens")
    event = relationship("Events")

    @property
    def serialize(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'id_telegram': self.id_telegram,
            'role': self.role,
            'is_archive': self.is_archive
        }


class MediaContens(Base):
    __tablename__ = "media_contents"

    id_media = Column(Integer, primary_key=True)
    id_type_media = Column(Integer, ForeignKey("type_media.id_type_media"))
    local_path = Column(String(250), nullable=False)
    description = Column(Text)
    date_download = Column(DateTime, nullable=False, default=datetime.datetime.now)
    last_time_used = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    remove = Column(Boolean, nullable=False, default=False)
    event = relationship("Events")
    tags = relationship("MediaTags")


class TypeMedia(Base):
    __tablename__ = "type_media"

    id_type_media = Column(Integer, primary_key=True)
    type_media = Column(String(20), nullable=False)
    path_dir = Column(String(250), nullable=False)
    extension = Column(String(20), nullable=False, unique=True)
    media_contents = relationship("MediaContens")

    @property
    def serialize(self):
        return {
            'id_type_media': self.id_type_media,
            'type_media': self.type_media,
            'path_dir': self.path_dir,
            'extension': self.extension
        }

class MediaTags(Base):
    __tablename__ = "media_tags"
    id_media_tags = Column(Integer, primary_key=True)
    id_tag = Column(Integer, ForeignKey("tags.id_tag"), nullable=False)
    id_media = Column(Integer, ForeignKey("media_contents.id_media"), nullable=False)


class Tags(Base):
    __tablename__ = "tags"

    id_tag = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    tags = relationship("MediaTags")


class Events(Base):
    __tablename__ = "events"

    id_event = Column(Integer, primary_key=True)
    id_message = Column(Integer, nullable=False, default=0)
    id_media = Column(Integer, ForeignKey("media_contents.id_media"), nullable=False)
    id_chanel = Column(Integer, ForeignKey("chanels.id_chanel"), nullable=False)
    caption = Column(Text)
    date_start = Column(DateTime, nullable=False, default=datetime.datetime.now)
    date_stop = Column(DateTime)
    completed = Column(Boolean, nullable=False, default=False)
    id_user = Column(Integer, ForeignKey("users.id_user"))


class Chanels(Base):
    __tablename__ = "chanels"

    id_chanel = Column(Integer, primary_key=True)
    name_chanel = Column(String(100), nullable=False)
    link_chanel = Column(String(100), nullable=False, default="no_name")
    id_telegram = Column(String(100), nullable=False, unique=True)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
    date_update = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    media_contents = relationship("Events")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
