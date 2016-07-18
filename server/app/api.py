
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sql', echo=True)

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    email_id = Column(String)
    email_object = Column(String)
    email_senders = Column(String)
    action = Column(String)

    def __repr__(self):
        return "<Log(created_at='{created_at}'>".format(created_at=self.created_at)

    def from_dict(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def as_dict(self):
        return {
                col.name: getattr(self, col.name)
                if col.name != 'created_at'
                else getattr(self, col.name).isoformat("T") + "Z"
                for col in self.__table__.columns
                }


# Create the Log table if it does not exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def logs_get(created_at_from=None, created_at_to=None):
    """Get all logs between `create_at_from` and `create_at_to`

    Args:
        created_at_from (string): Date from which logs are created, ignored if None (default)
        created_at_to (string): Date until which logs are created, ignored if None (default)


    Returns:
        list of dict: List of log objects
    """
    try:
        # Convert from RFC3339 to a Datetime object
        if created_at_from:
            created_at_from = datetime.datetime.strptime(created_at_from, '%Y-%m-%dT%H:%M:%S.%fZ')
        if created_at_to:
            created_at_to = datetime.datetime.strptime(created_at_to, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        created_at_from = None
        created_at_to = None

    if created_at_from and created_at_to:
        log_objects = session.query(Log).filter(Log.created_at.between(created_at_from, created_at_to))
    elif created_at_from:
        log_objects = session.query(Log).filter(Log.created_at >= created_at_from)
    elif created_at_to:
        log_objects = session.query(Log).filter(Log.created_at <= created_at_to)
    else:
        log_objects = session.query(Log)
    logs = [log_object.as_dict() for log_object in log_objects]
    return logs, 200

# Be careful, the argument should be named as per the swagger.yaml file, but the name is case sensitive.
def logs_post(log):
    """Create a new Log

    Returns:
        dict: log object
    """
    log.pop('id')
    log.pop('created_at')
    log_object = Log()
    log_object.from_dict(**log)
    session.add(log_object)
    session.commit()
    return log_object.as_dict(), 201
