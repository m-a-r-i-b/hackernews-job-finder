import React, { useState, useEffect } from 'react';
import { Table, Modal } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useSocket } from '../../SocketContext';
import { columns } from './Columns';
import { parseComment } from './CommentParser';

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
        let commentsList = Object.entries(commentsDict).map(([key, value]) => ({ key, ...value }));
        console.log("comments List = ",commentsList)
        commentsList.forEach((comment) =>  parseComment(comment));
        console.log("Parsed comments List = ",commentsList)
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
        const updatedComment = parseComment(JSON.parse(event.data));
        console.log("Updated comment = ", updatedComment)
        setDataSource((dataSource) =>
          dataSource.map((comment) => 
            comment.key === updatedComment.comment_id ? { ...comment,...updatedComment, ...updatedComment.payload }  : comment
          )
        );

      };
    }
  }, [socket]);

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
            <p>Comment Id: {selectedRow.key}</p>
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
