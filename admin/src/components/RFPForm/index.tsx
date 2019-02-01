import React from 'react';
import { view } from 'react-easy-state';
import { RouteComponentProps, withRouter } from 'react-router';
import { Form, Input, Select, Icon, Button, message, Spin } from 'antd';
import Exception from 'ant-design-pro/lib/Exception';
import { FormComponentProps } from 'antd/lib/form';
import { PROPOSAL_CATEGORY, RFP_STATUS, RFPArgs } from 'src/types';
import { CATEGORY_UI } from 'util/ui';
import { typedKeys } from 'util/ts';
import { RFP_STATUSES, getStatusById } from 'util/statuses';
import Markdown from 'components/Markdown';
import Back from 'components/Back';
import store from 'src/store';
import './index.less';

type Props = FormComponentProps & RouteComponentProps<{ id?: string }>;

interface State {
  isShowingPreview: boolean;
}

class RFPForm extends React.Component<Props, State> {
  state: State = {
    isShowingPreview: false,
  };

  constructor(props: Props) {
    super(props);
    const rfpId = this.getRFPId();
    if (rfpId && !store.rfpsFetched) {
      store.fetchRFPs();
    }
  }

  render() {
    const { isShowingPreview } = this.state;
    const { getFieldDecorator, getFieldValue } = this.props.form;

    let defaults: RFPArgs = {
      title: '',
      brief: '',
      content: '',
      category: '',
      status: '',
    };
    const rfpId = this.getRFPId();
    if (rfpId) {
      if (!store.rfpsFetched) {
        return <Spin />;
      }

      const rfp = store.rfps.find(r => r.id === rfpId);
      if (rfp) {
        defaults = {
          title: rfp.title,
          brief: rfp.brief,
          content: rfp.content,
          category: rfp.category,
          status: rfp.status,
        };
      } else {
        return <Exception type="404" desc="This RFP does not exist" />;
      }
    }

    return (
      <Form className="RFPForm" layout="vertical" onSubmit={this.handleSubmit}>
        <Back to="/rfps" text="RFPs" />
        <Form.Item label="Title">
          {getFieldDecorator('title', {
            initialValue: defaults.title,
            rules: [
              { required: true, message: 'Title is required' },
              { max: 60, message: 'Max 60 chars' },
            ],
          })(
            <Input
              autoComplete="off"
              name="title"
              placeholder="Max 60 chars"
              size="large"
              autoFocus
            />,
          )}
        </Form.Item>

        {rfpId && (
          <Form.Item label="Status">
            {getFieldDecorator('status', {
              initialValue: defaults.status,
              rules: [{ required: true, message: 'Status is required' }],
            })(
              <Select size="large" placeholder="Select a status">
                {typedKeys(RFP_STATUS).map(c => (
                  <Select.Option value={c} key={c}>
                    {getStatusById(RFP_STATUSES, c).tagDisplay}
                  </Select.Option>
                ))}
              </Select>,
            )}
          </Form.Item>
        )}

        <Form.Item label="Category">
          {getFieldDecorator('category', {
            initialValue: defaults.category,
            rules: [
              { required: true, message: 'Category is required' },
              { max: 60, message: 'Max 60 chars' },
            ],
          })(
            <Select size="large" placeholder="Select a category">
              {typedKeys(PROPOSAL_CATEGORY).map(c => (
                <Select.Option value={c} key={c}>
                  <Icon
                    type={CATEGORY_UI[c].icon}
                    style={{ color: CATEGORY_UI[c].color }}
                  />{' '}
                  {CATEGORY_UI[c].label}
                </Select.Option>
              ))}
            </Select>,
          )}
        </Form.Item>

        <Form.Item label="Brief description">
          {getFieldDecorator('brief', {
            initialValue: defaults.brief,
            rules: [
              { required: true, message: 'Title is required' },
              { max: 200, message: 'Max 200 chars' },
            ],
          })(<Input.TextArea rows={3} name="brief" placeholder="Max 200 chars" />)}
        </Form.Item>

        <Form.Item className="RFPForm-content" label="Content" required>
          {/* Keep rendering even while hiding to not reset value */}
          <div style={{ display: isShowingPreview ? 'none' : 'block' }}>
            {getFieldDecorator('content', {
              initialValue: defaults.content,
              rules: [{ required: true, message: 'Content is required' }],
            })(
              <Input.TextArea
                rows={8}
                name="content"
                placeholder="Preview will appear on the right"
                autosize={{ minRows: 6, maxRows: 15 }}
              />,
            )}
          </div>
          {isShowingPreview ? (
            <>
              <div className="RFPForm-content-preview">
                <Markdown source={getFieldValue('content') || '_No content_'} />
              </div>
              <a className="RFPForm-content-previewToggle" onClick={this.togglePreview}>
                Edit content
              </a>
            </>
          ) : (
            <a className="RFPForm-content-previewToggle" onClick={this.togglePreview}>
              Preview content
            </a>
          )}
        </Form.Item>

        <div className="RFPForm-buttons">
          <Button type="primary" htmlType="submit" size="large">
            Submit
          </Button>
          <Button type="ghost" size="large">
            Cancel
          </Button>
        </div>
      </Form>
    );
  }

  private getRFPId = () => {
    const rfpId = this.props.match.params.id;
    if (rfpId) {
      return parseInt(rfpId, 10);
    }
  };

  private togglePreview = () => {
    this.setState({ isShowingPreview: !this.state.isShowingPreview });
  };

  private handleSubmit = (ev: React.FormEvent<HTMLFormElement>) => {
    ev.preventDefault();
    this.props.form.validateFieldsAndScroll(async (err: any, values: any) => {
      if (err) return;

      const rfpId = this.getRFPId();
      let msg;
      if (rfpId) {
        await store.editRFP(rfpId, values);
        msg = 'Successfully updated RFP';
      } else {
        await store.createRFP(values);
        msg = 'Successfully created RFP. To publish, edit it and set status to "Live"';
      }

      if (store.rfpSaved) {
        message.success(msg, 3);
        this.props.history.replace('/rfps');
      }
    });
  };
}

export default Form.create()(withRouter(view(RFPForm)));