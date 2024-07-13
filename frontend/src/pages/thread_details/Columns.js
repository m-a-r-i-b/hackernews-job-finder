import { Tag } from 'antd';

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
    title: 'Allows Remote Work',
    dataIndex: 'IS_REMOTE_WORK_ALLOWED',
    key: 'IS_REMOTE_WORK_ALLOWED',
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
      return keywords.split(',').map((keyword, index) => (
        <Tag key={index} color="blue">
          {keyword.trim()}
        </Tag>
      ));
    },
  },
  {
    title: 'Contact Info',
    dataIndex: 'EXTRACT_CONTRACT_INFO',
    key: 'EXTRACT_CONTRACT_INFO',
  },
];