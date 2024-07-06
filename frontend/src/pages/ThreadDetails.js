import React, { useState } from 'react';
import { Table, Modal } from 'antd';
import { useParams } from 'react-router-dom';

const ThreadDetails = () => {
  const { title } = useParams();
  const [visible, setVisible] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);

  const dataSource = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
    },
  ];

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
    },
  ];

  const handleRowClick = (record) => {
    setSelectedRow(record);
    setVisible(true);
  };

  const handleCancel = () => {
    setVisible(false);
    setSelectedRow(null);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>YOOO</h1>
      <Table
        dataSource={dataSource}
        columns={columns}
        onRow={(record) => ({
          onClick: () => handleRowClick(record),
        })}
      />
      <Modal
        title="Row Details"
        visible={visible}
        onCancel={handleCancel}
        onOk={handleCancel}
      >
        {selectedRow && (
          <div>
            <p>Name: {selectedRow.name}</p>
            <p>Age: {selectedRow.age}</p>
            <p>Address: {selectedRow.address}</p>
          </div>
        )}
      </Modal>
      <h1>BYEE</h1>
    </div>
  );
};

export default ThreadDetails;
