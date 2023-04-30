from app import db
from sqlalchemy.ext.associationproxy import association_proxy


# -------------------------- Associations --------------------------#
class UserRecipientList(db.Model):
    """
    Represents many-to-many relationship between user and recipient lists
    """

    __tablename__ = "user_recipient_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    recipient_list_id = db.Column(
        "recipient_list_id", db.Integer, db.ForeignKey("recipient_list.id")
    )
    role = db.Column(db.String)

    user = db.relationship("User", back_populates="recipient_list_association")
    recipient_list = db.relationship("RecipientList", back_populates="user_association")


class UserEvent(db.Model):
    """
    Represents many-to-many relationship between user and event
    """

    __tablename__ = "user_event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column("event_id", db.Integer, db.ForeignKey("event.id"))
    role = db.Column(db.String)

    user = db.relationship("User", back_populates="event_association")
    event = db.relationship("Event", back_populates="user_association")


# ----------------------------- Models -----------------------------#
class User(db.Model):
    """
    User model (One-to-many relation to Recipient lists)
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User information
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.LargeBinary, nullable=False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    # Define many-to-many relationships
    event_association = db.relationship("UserEvent", back_populates="user")
    events = association_proxy("event_association", "event")
    recipient_list_association = db.relationship(
        "UserRecipientList", back_populates="user"
    )
    recipient_lists = association_proxy("recipient_list_association", "recipient_list")

    def __init__(self, **kwargs):
        """
        Initializes a Course object
        """

        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.password_digest = kwargs.get("password_digest")


class Event(db.Model):
    """
    Event model (One-to-Many relation with User)
    """

    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    user_association = db.relationship("UserEvent", back_populates="event")
    users = association_proxy("user_association", "user")

    def __init__(self, **kwargs):
        """
        Initializes an event object
        """

        self.name = kwargs.get("name")
        self.creator_id = kwargs.get("creator_id")


class RecipientList(db.Model):
    """
    Recipient list model (One-to-Many relation with User)
    """

    __tablename__ = "recipient_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    # Has one corresponding creator_id
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Users in the recipient list
    user_association = db.relationship(
        "UserRecipientList", back_populates="recipient_list"
    )
    # Define proxy to bypass intermediate transaction with a UserRecipientList association object
    users = association_proxy("user_association", "user")

    def __init__(self, **kwargs):
        """
        Initializes an recipient list object
        """

        self.title = kwargs.get("title")
        self.creator_id = kwargs.get("creator_id")


# TODO: Community model? Implement events in a community, which can be assessed and seen by only users within that community? Can be public or more specific
