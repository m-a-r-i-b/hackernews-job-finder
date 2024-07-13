import React, { useState, useEffect } from 'react';
import { Table, Modal } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useSocket } from '../SocketContext';

const ThreadDetails = () => {
  const { url } = useParams();
  const [visible, setVisible] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [dataSource, setDataSource] = useState([]);
  const socket = useSocket();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const decodedUrl = atob(url);
        const response = await axios.get(`http://127.0.0.1:8000/get-thread-by-url/?url=${decodedUrl}`);
        const commentsDict = response.data.comments;
        const commentsList = Object.entries(commentsDict).map(([key, value]) => ({ key, ...value }));
        console.log("comments List = ",commentsList)
        setDataSource(commentsList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [url]);

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        console.log("socket event data = ", event.data)
        const updatedComment = JSON.parse(event.data);

        if (updatedComment.payload){
          if (updatedComment.payload.IS_REMOTE_WORK_ALLOWED){
            // Check if If updatedComment.payload.IS_REMOTE_WORK_ALLOWED is of type object, 
            // extract allows_remote_work key and assign it to IS_REMOTE_WORK_ALLOWED
            // Otherwise dont change anything
            if (typeof updatedComment.payload.IS_REMOTE_WORK_ALLOWED === 'object'){
              updatedComment.payload.IS_REMOTE_WORK_ALLOWED = String(updatedComment.payload.IS_REMOTE_WORK_ALLOWED.allows_remote_work)
            }
          }
        }


        console.log("Parsed comment = ", updatedComment)
        setDataSource((dataSource) =>
          dataSource.map((comment) => 
            comment.key === updatedComment.comment_id ? { ...comment,...updatedComment, ...updatedComment.payload }  : comment
          )
        );

      };
    }
  }, [socket]);

  const columns = [
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
    },
    {
      title: 'categorize',
      dataIndex: 'categorize',
      key: 'categorize',
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
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        onRow={(record) => ({
          onClick: () => handleRowClick(record),
        })}
      />
      <Modal
        title="Row Details"
        open={visible}
        onCancel={handleCancel}
        onOk={handleCancel}
      >
        {selectedRow && (
          <div>
            <p>Key: {selectedRow.key}</p>
            <p>Text: {selectedRow.text}</p>
            <p>Filter: {selectedRow.filter}</p>
            <p>Categorize: {selectedRow.categorize}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ThreadDetails;
