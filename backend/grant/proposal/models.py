import datetime

from grant.comment.models import Comment
from grant.extensions import ma, db
from grant.utils.misc import dt_to_unix

FUNDING_REQUIRED = 'FUNDING_REQUIRED'
COMPLETED = 'COMPLETED'
PROPOSAL_STAGES = [FUNDING_REQUIRED, COMPLETED]

DAPP = "DAPP"
DEV_TOOL = "DEV_TOOL"
CORE_DEV = "CORE_DEV"
COMMUNITY = "COMMUNITY"
DOCUMENTATION = "DOCUMENTATION"
ACCESSIBILITY = "ACCESSIBILITY"
CATEGORIES = [DAPP, DEV_TOOL, CORE_DEV, COMMUNITY, DOCUMENTATION, ACCESSIBILITY]


class ValidationException(Exception):
    pass


proposal_team = db.Table(
    'proposal_team', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('proposal_id', db.Integer, db.ForeignKey('proposal.id'))
)


class Proposal(db.Model):
    __tablename__ = "proposal"

    id = db.Column(db.Integer(), primary_key=True)
    date_created = db.Column(db.DateTime)

    title = db.Column(db.String(255), nullable=False)
    proposal_id = db.Column(db.String(255), unique=True, nullable=False)
    stage = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    team = db.relationship("User", secondary=proposal_team)
    comments = db.relationship(Comment, backref="proposal", lazy=True)
    milestones = db.relationship("Milestone", backref="proposal", lazy=True)

    def __init__(
            self,
            stage: str,
            proposal_id: str,
            title: str,
            content: str,
            category: str
    ):
        self.stage = stage
        self.proposal_id = proposal_id
        self.title = title
        self.content = content
        self.category = category
        self.date_created = datetime.datetime.now()

    @staticmethod
    def validate(
            stage: str,
            proposal_id: str,
            title: str,
            content: str,
            category: str):
        if stage not in PROPOSAL_STAGES:
            raise ValidationException("{} not in {}".format(stage, PROPOSAL_STAGES))
        if category not in CATEGORIES:
            raise ValidationException("{} not in {}".format(category, CATEGORIES))

    @staticmethod
    def create(**kwargs):
        Proposal.validate(**kwargs)
        return Proposal(
            **kwargs
        )


class ProposalSchema(ma.Schema):
    class Meta:
        model = Proposal
        # Fields to expose
        fields = (
            "stage",
            "date_created",
            "title",
            "proposal_id",
            "body",
            "comments",
            "milestones",
            "category",
            "team"
        )

    date_created = ma.Method("get_date_created")
    proposal_id = ma.Method("get_proposal_id")
    body = ma.Method("get_body")

    comments = ma.Nested("CommentSchema", many=True)
    team = ma.Nested("UserSchema", many=True)
    milestones = ma.Nested("MilestoneSchema", many=True)

    def get_body(self, obj):
        return obj.content

    def get_proposal_id(self, obj):
        return obj.proposal_id

    def get_date_created(self, obj):
        return dt_to_unix(obj.date_created)


proposal_schema = ProposalSchema()
proposals_schema = ProposalSchema(many=True)