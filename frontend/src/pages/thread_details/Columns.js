import { Tag } from 'antd';
import { assignColorToKeyword } from '../../Utils';
import { Checkbox } from 'antd';
import axios from 'axios';


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
    filters: [
      { text: 'Yes', value: 'true' },
      { text: 'No', value: 'false' },
    ],
    onFilter: (value, record) => record.IS_REMOTE_WORK_ALLOWED === value,
    render: (value) => {
      if (value === undefined || value === null) {
        return '';
      }
      return (
        <Tag color={value == 'true' ? 'green' : 'red'}>
          {value == 'true' ? 'YES' : 'NO'}
        </Tag>
      );
    },
  },
  {
    title: 'Role',
    dataIndex: 'EXTRACT_ROLES',
    key: 'EXTRACT_ROLES',
  },
  {
    title: 'Keywords',
    dataIndex: 'EXTRACT_KEYWORDS',
    key: 'EXTRACT_KEYWORDS',
    render: (keywords) => {
      if (!keywords) {
        return '';
      }
      return keywords.split(',').map((keyword, index) => {
        const trimmedKeyword = keyword.trim().toLowerCase();
        let languageColor = assignColorToKeyword(trimmedKeyword);

        return (
          <Tag key={index} color={languageColor || 'default'}>
            {keyword.trim()}
          </Tag>
        );
      });
    },
  },
  {
    title: 'Contact Info',
    dataIndex: 'EXTRACT_CONTRACT_INFO',
    key: 'EXTRACT_CONTRACT_INFO',
  },
  {
    title: 'Action',
    key: 'action',
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
  // Update local state
  const url = window.location.href.split("/").pop();
  const decodedUrl = atob(url);
  console.log("decoded url = ",decodedUrl)
  console.log('record', record);

  try {
    await axios.post(`http://127.0.0.1:8000/update-comment-read-status`, {
      thread_url: decodedUrl,
      comment_id: record.key,
      is_read: checked,
    });
    console.log(`Comment ${record.key} read status updated successfully!`);
  } catch (error) {
    console.error('Error updating read status:', error);
    // Handle error state or retry logic here
  }
};