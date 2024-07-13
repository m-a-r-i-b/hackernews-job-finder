import { Checkbox } from 'antd';
import axios from 'axios';
import { remoteWorkColumnRenderer } from '../../components/column_renderers/RemoteWorkAllowed';
import { roleRenderer } from '../../components/column_renderers/Role';
import { keyworkRenderer } from '../../components/column_renderers/Keyword';
import { contactInfoRenderer } from '../../components/column_renderers/ContactInfo';
import { BASE_URL } from '../../Constants';

export const columns = [
  {
    title: 'Id',
    dataIndex: 'key',
    width: 100,
    key: 'key',
  },
  {
    title: 'Comment',
    dataIndex: 'text',
    key: 'text',
    width: 300,
    ellipsis: true,
  },
  {
    title: 'Remote',
    dataIndex: 'IS_REMOTE_WORK_ALLOWED',
    key: 'IS_REMOTE_WORK_ALLOWED',
    width: 120,
    ellipsis: true,
    filters: [
      { text: 'Yes', value: 'true' },
      { text: 'No', value: 'false' },
    ],
    onFilter: (value, record) => record.IS_REMOTE_WORK_ALLOWED === value,
    render: (value) => remoteWorkColumnRenderer(value),
  },
  {
    title: 'Role',
    dataIndex: 'EXTRACT_ROLES',
    key: 'EXTRACT_ROLES',
    render: (value) => roleRenderer(value),
  },
  {
    title: 'Keywords',
    dataIndex: 'EXTRACT_KEYWORDS',
    key: 'EXTRACT_KEYWORDS',
    render: (keywords) => keyworkRenderer(keywords),
  },
  {
    title: 'Contact Info',
    dataIndex: 'EXTRACT_CONTACT_INFO',
    key: 'EXTRACT_CONTACT_INFO',
    render: (value) => contactInfoRenderer(value),
  },
  {
    title: 'Is Read',
    key: 'action',
    filters: [
      { text: 'Read', value: true },
      { text: 'Unread', value: false },
    ],
    onFilter: (value, record) => {
      if (value === true) {
        return record.is_read === value;
      }

      if (value === false) {
        return record.is_read === value || record.is_read === undefined;
      }

    },
    render: (text, record) => (
      <Checkbox
        checked={record.is_read} // Assuming 'read' is a property in your data
        onClick={(e) => e.stopPropagation()} // Stop event propagation to prevent triggering
        onChange={(e) => handleCheckboxChange(record, e.target.checked)}
      />
    ),
  },
];


const handleCheckboxChange = async (record, checked) => {
  const url = window.location.href.split("/").pop();
  const decodedUrl = atob(url);

  try {
    await axios.post(`${BASE_URL}/update-comment-read-status`, {
      thread_url: decodedUrl,
      comment_id: record.key,
      is_read: checked,
    });
    console.log(`Comment ${record.key} read status updated successfully!`);
  } catch (error) {
    console.error('Error updating read status:', error);
  }
};