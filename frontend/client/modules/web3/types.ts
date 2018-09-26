enum web3Types {
  WEB3 = 'WEB3',
  WEB3_FULFILLED = 'WEB3_FULFILLED',
  WEB3_REJECTED = 'WEB3_REJECTED',
  WEB3_PENDING = 'WEB3_PENDING',

  CONTRACT = 'CONTRACT',
  CONTRACT_FULFILLED = 'CONTRACT_FULFILLED',
  CONTRACT_REJECTED = 'CONTRACT_REJECTED',
  CONTRACT_PENDING = 'CONTRACT_PENDING',

  CROWD_FUND = 'CROWD_FUND',
  CROWD_FUND_FULFILLED = 'CROWD_FUND_FULFILLED',
  CROWD_FUND_REJECTED = 'CROWD_FUND_REJECTED',
  CROWD_FUND_PENDING = 'CROWD_FUND_PENDING',
  CROWD_FUND_CREATED = 'CROWD_FUND_CREATED',
  RESET_CROWD_FUND = 'RESET_CROWD_FUND',

  SEND = 'SEND',
  SEND_FULFILLED = 'SEND_FULFILLED',
  SEND_REJECTED = 'SEND_REJECTED',
  SEND_PENDING = 'SEND_PENDING',

  PAY_MILESTONE_PAYOUT = 'PAY_MILESTONE_PAYOUT',
  PAY_MILESTONE_PAYOUT_FULFILLED = 'PAY_MILESTONE_PAYOUT_FULFILLED',
  PAY_MILESTONE_PAYOUT_REJECTED = 'PAY_MILESTONE_PAYOUT_REJECTED',
  PAY_MILESTONE_PAYOUT_PENDING = 'PAY_MILESTONE_PAYOUT_PENDING',

  REQUEST_MILESTONE_PAYOUT = 'REQUEST_MILESTONE_PAYOUT',
  REQUEST_MILESTONE_PAYOUT_FULFILLED = 'REQUEST_MILESTONE_PAYOUT_FULFILLED',
  REQUEST_MILESTONE_PAYOUT_REJECTED = 'REQUEST_MILESTONE_PAYOUT_REJECTED',
  REQUEST_MILESTONE_PAYOUT_PENDING = 'REQUEST_MILESTONE_PAYOUT_PENDING',

  VOTE_AGAINST_MILESTONE_PAYOUT = 'VOTE_AGAINST_MILESTONE_PAYOUT',
  VOTE_AGAINST_MILESTONE_PAYOUT_FULFILLED = 'VOTE_AGAINST_MILESTONE_PAYOUT_FULFILLED',
  VOTE_AGAINST_MILESTONE_PAYOUT_REJECTED = 'VOTE_AGAINST_MILESTONE_PAYOUT_REJECTED',
  VOTE_AGAINST_MILESTONE_PAYOUT_PENDING = 'VOTE_AGAINST_MILESTONE_PAYOUT_PENDING',

  VOTE_REFUND = 'VOTE_REFUND',
  VOTE_REFUND_FULFILLED = 'VOTE_REFUND_FULFILLED',
  VOTE_REFUND_REJECTED = 'VOTE_REFUND_REJECTED',
  VOTE_REFUND_PENDING = 'VOTE_REFUND_PENDING',

  WITHDRAW_REFUND = 'WITHDRAW_REFUND',
  WITHDRAW_REFUND_FULFILLED = 'WITHDRAW_REFUND_FULFILLED',
  WITHDRAW_REFUND_REJECTED = 'WITHDRAW_REFUND_REJECTED',
  WITHDRAW_REFUND_PENDING = 'WITHDRAW_REFUND_PENDING',

  TRIGGER_REFUND = 'TRIGGER_REFUND',
  TRIGGER_REFUND_FULFILLED = 'TRIGGER_REFUND_FULFILLED',
  TRIGGER_REFUND_REJECTED = 'TRIGGER_REFUND_REJECTED',
  TRIGGER_REFUND_PENDING = 'TRIGGER_REFUND_PENDING',

  ACCOUNTS = 'ACCOUNTS',
  ACCOUNTS_FULFILLED = 'ACCOUNTS_FULFILLED',
  ACCOUNTS_REJECTED = 'ACCOUNTS_REJECTED',
  ACCOUNTS_PENDING = 'ACCOUNTS_PENDING',

  SIGN_DATA = 'SIGN_DATA',
  SIGN_DATA_FULFILLED = 'SIGN_DATA_FULFILLED',
  SIGN_DATA_REJECTED = 'SIGN_DATA_REJECTED',
  SIGN_DATA_PENDING = 'SIGN_DATA_PENDING',

  SET_WRONG_NETWORK = 'SET_WRONG_NETWORK',
  SET_WEB3_LOCKED = 'SET_WEB3_LOCKED',
}

export default web3Types;