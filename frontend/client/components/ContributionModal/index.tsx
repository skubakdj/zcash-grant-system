import React from 'react';
import { Link } from 'react-router-dom';
import { Modal, Alert } from 'antd';
import Result from 'ant-design-pro/lib/Result';
import { postProposalContribution, getProposalContribution } from 'api/api';
import { ContributionWithAddressesAndUser } from 'types';
import PaymentInfo from './PaymentInfo';

interface OwnProps {
  isVisible: boolean;
  contribution?: ContributionWithAddressesAndUser | Falsy;
  proposalId?: number;
  contributionId?: number;
  amount?: string;
  isAnonymous?: boolean;
  hasNoButtons?: boolean;
  text?: React.ReactNode;
  handleClose(): void;
}

type Props = OwnProps;

interface State {
  hasConfirmedAnonymous: boolean;
  hasSent: boolean;
  contribution: ContributionWithAddressesAndUser | null;
  error: string | null;
}

export default class ContributionModal extends React.Component<Props, State> {
  state: State = {
    hasConfirmedAnonymous: true,
    hasSent: false,
    contribution: null,
    error: null,
  };

  constructor(props: Props) {
    super(props);
    if (props.isAnonymous) {
      this.state = {
        ...this.state,
        hasConfirmedAnonymous: false,
      };
    }
    if (props.contribution) {
      this.state = {
        ...this.state,
        contribution: props.contribution,
        hasConfirmedAnonymous: !!props.contribution.user.userid,
      };
    }
  }

  componentWillUpdate(nextProps: Props, nextState: State) {
    const {
      isVisible,
      proposalId,
      contributionId,
      contribution,
      isAnonymous,
    } = nextProps;
    let { hasConfirmedAnonymous } = nextState;
    // If we're opening the modal, set hasConfirmedAnonymous based on isAnonymous
    if (isVisible && !this.props.isVisible && isAnonymous && !hasConfirmedAnonymous) {
      hasConfirmedAnonymous = false;
      this.setState({ hasConfirmedAnonymous: false });
    }
    // When modal is opened and proposalId is provided or changed and we've confirmed anonymity
    if (isVisible && proposalId && hasConfirmedAnonymous) {
      if (this.props.isVisible !== isVisible || proposalId !== this.props.proposalId) {
        this.fetchAddresses(proposalId, contributionId);
      }
    }
    // If contribution is provided, update it
    if (contribution !== this.props.contribution) {
      this.setState({
        contribution: contribution || null,
        hasConfirmedAnonymous: contribution
          ? !!contribution.user.userid
          : nextState.hasConfirmedAnonymous,
      });
    }
  }

  render() {
    const { isVisible, handleClose, hasNoButtons, text } = this.props;
    const { hasSent, hasConfirmedAnonymous, contribution, error } = this.state;
    let okText;
    let onOk;
    let content;

    if (!hasConfirmedAnonymous) {
      okText = 'I accept';
      onOk = this.confirmAnonymous;
      content = (
        <Alert
          className="PaymentInfo-anonymous"
          type="warning"
          message="This contribution is anonymous"
          description={
            <>
              You are about to contribute anonymously. Your contribution will show up
              without attribution, and even if you're logged in,{' '}
              <strong>will not appear anywhere on your account</strong> after you close
              this modal.
              <br /> <br />
              In the case of a refund, your contribution will be treated as a donation to
              the Zcash Foundation instead.
              <br /> <br />
              If you would like to have your contribution attached to an account, just
              close this, make sure you're logged in, and don't check the "Contribute
              anonymously" checkbox.
            </>
          }
        />
      );
    } else if (hasSent) {
      okText = 'Done';
      onOk = handleClose;
      content = (
        <Result
          type="success"
          title="Thank you for your contribution!"
          description={
            <>
              Your contribution should be confirmed in about 20 minutes. You can keep an
              eye on it at the{' '}
              <Link to="/profile?tab=funded">funded tab on your profile</Link>.
            </>
          }
          style={{ width: '90%' }}
        />
      );
    } else {
      if (error) {
        okText = 'Done';
        onOk = handleClose;
        content = error;
      } else {
        okText = 'I’ve sent it';
        onOk = this.confirmSend;
        content = <PaymentInfo contribution={contribution} text={text} />;
      }
    }

    return (
      <Modal
        title="Make your contribution"
        visible={isVisible}
        closable={hasSent || hasNoButtons}
        maskClosable={hasSent || hasNoButtons}
        okText={okText}
        onOk={onOk}
        onCancel={handleClose}
        footer={hasNoButtons ? '' : undefined}
        centered
      >
        {content}
      </Modal>
    );
  }

  private async fetchAddresses(proposalId: number, contributionId?: number) {
    try {
      const { amount, isAnonymous } = this.props;
      let res;
      if (contributionId) {
        res = await getProposalContribution(proposalId, contributionId);
      } else {
        res = await postProposalContribution(proposalId, amount || '0', isAnonymous);
      }
      this.setState({ contribution: res.data });
    } catch (err) {
      this.setState({ error: err.message });
    }
  }

  private confirmAnonymous = () => {
    this.setState({ hasConfirmedAnonymous: true });
  };

  private confirmSend = () => {
    this.setState({ hasSent: true });
  };
}
