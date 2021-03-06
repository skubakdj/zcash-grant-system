from datetime import datetime, timedelta

from grant.extensions import db
from grant.email.send import send_email
from grant.utils.enums import ProposalStage, ContributionStatus, ProposalStatus
from grant.utils.misc import make_url
from flask import current_app


class ProposalReminder:
    JOB_TYPE = 1

    def __init__(self, proposal_id):
        self.proposal_id = proposal_id

    def blobify(self):
        return {"proposal_id": self.proposal_id}

    def make_task(self):
        from .models import Task
        task = Task(
            job_type=self.JOB_TYPE,
            blob=self.blobify(),
            execute_after=datetime.now()
        )
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def process_task(task):
        assert task.job_type == 1, "Job type: {} is incorrect for ProposalReminder".format(task.job_type)
        from grant.proposal.models import Proposal
        proposal = Proposal.query.filter_by(id=task.blob["proposal_id"]).first()
        print(proposal)
        task.completed = True
        db.session.add(task)
        db.session.commit()


class ProposalDeadline:
    JOB_TYPE = 2

    def __init__(self, proposal):
        self.proposal = proposal

    def blobify(self):
        return {
            "proposal_id": self.proposal.id,
        }

    def make_task(self):
        from .models import Task
        task = Task(
            job_type=self.JOB_TYPE,
            blob=self.blobify(),
            execute_after=self.proposal.date_published + timedelta(seconds=self.proposal.deadline_duration),
        )
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def process_task(task):
        from grant.proposal.models import Proposal
        proposal = Proposal.query.filter_by(id=task.blob["proposal_id"]).first()

        # If it was deleted, canceled, or successful, just noop out
        if not proposal or proposal.is_funded or proposal.stage != ProposalStage.FUNDING_REQUIRED:
            return

        # Otherwise, mark it as failed and inform everyone
        proposal.stage = ProposalStage.FAILED
        db.session.add(proposal)
        db.session.commit()

        # Send emails to team & contributors
        for u in proposal.team:
            send_email(u.email_address, 'proposal_failed', {
                'proposal': proposal,
            })
        for u in proposal.contributors:
            send_email(u.email_address, 'contribution_proposal_failed', {
                'proposal': proposal,
                'refund_address': u.settings.refund_address,
                'account_settings_url': make_url('/profile/settings?tab=account')
            })


class ContributionExpired:
    JOB_TYPE = 3

    def __init__(self, contribution):
        self.contribution = contribution

    def blobify(self):
        return {
            "contribution_id": self.contribution.id,
        }

    def make_task(self):
        from .models import Task
        task = Task(
            job_type=self.JOB_TYPE,
            blob=self.blobify(),
            execute_after=self.contribution.date_created + timedelta(hours=24),
        )
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def process_task(task):
        from grant.proposal.models import ProposalContribution
        contribution = ProposalContribution.query.filter_by(id=task.blob["contribution_id"]).first()

        # If it's missing or not pending, noop out
        if not contribution or contribution.status != ContributionStatus.PENDING:
            return

        # Otherwise, inform the user (if not anonymous)
        if contribution.user:
            send_email(contribution.user.email_address, 'contribution_expired', {
                'contribution': contribution,
                'proposal': contribution.proposal,
                'contact_url': make_url('/contact'),
                'profile_url': make_url(f'/profile/{contribution.user.id}'),
                'proposal_url': make_url(f'/proposals/{contribution.proposal.id}'),
            })


class PruneDraft:
    JOB_TYPE = 4
    PRUNE_TIME = 259200  # 72 hours in seconds

    def __init__(self, proposal):
        self.proposal = proposal

    def blobify(self):
        return {
            "proposal_id": self.proposal.id,
        }

    def make_task(self):
        from .models import Task

        task = Task(
            job_type=self.JOB_TYPE,
            blob=self.blobify(),
            execute_after=self.proposal.date_created + timedelta(seconds=self.PRUNE_TIME),
        )
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def process_task(task):
        from grant.proposal.models import Proposal, default_proposal_content
        proposal = Proposal.query.filter_by(id=task.blob["proposal_id"]).first()

        # If it was deleted or moved out of a draft, noop out
        if not proposal or proposal.status != ProposalStatus.DRAFT:
            return

        # If proposal content deviates from the default, noop out
        if proposal.content != default_proposal_content():
            return

        # If any of the remaining proposal fields are filled, noop out
        if proposal.title or proposal.brief or proposal.category or proposal.target != "0":
            return

        if proposal.payout_address or proposal.milestones:
            return

        # Otherwise, delete the empty proposal
        db.session.delete(proposal)
        db.session.commit()


class MilestoneDeadline:
    JOB_TYPE = 5

    def __init__(self, proposal, milestone):
        self.proposal = proposal
        self.milestone = milestone

    def blobify(self):
        from grant.proposal.models import ProposalUpdate

        update_count = len(ProposalUpdate.query.filter_by(proposal_id=self.proposal.id).all())
        return {
            "proposal_id": self.proposal.id,
            "milestone_id": self.milestone.id,
            "update_count": update_count
        }

    def make_task(self):
        from .models import Task
        task = Task(
            job_type=self.JOB_TYPE,
            blob=self.blobify(),
            execute_after=self.milestone.date_estimated,
        )
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def process_task(task):
        from grant.proposal.models import Proposal, ProposalUpdate
        from grant.milestone.models import Milestone

        proposal_id = task.blob["proposal_id"]
        milestone_id = task.blob["milestone_id"]
        update_count = task.blob["update_count"]

        proposal = Proposal.query.filter_by(id=proposal_id).first()
        milestone = Milestone.query.filter_by(id=milestone_id).first()
        current_update_count = len(ProposalUpdate.query.filter_by(proposal_id=proposal_id).all())

        # if proposal was deleted or cancelled, noop out
        if not proposal or proposal.status == ProposalStatus.DELETED or proposal.stage == ProposalStage.CANCELED:
            return

        # if milestone was deleted, noop out
        if not milestone:
            return

        # if milestone payout has been requested or an update has been posted, noop out
        if current_update_count > update_count or milestone.date_requested:
            return

        # send email to arbiter notifying milestone deadline has been missed
        send_email(proposal.arbiter.user.email_address, 'milestone_deadline', {
            'proposal': proposal,
            'proposal_milestones_url': make_url(f'/proposals/{proposal.id}?tab=milestones'),
        })


JOBS = {
    1: ProposalReminder.process_task,
    2: ProposalDeadline.process_task,
    3: ContributionExpired.process_task,
    4: PruneDraft.process_task,
    5: MilestoneDeadline.process_task
}
