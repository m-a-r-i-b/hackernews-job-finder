import React, { useState, useEffect } from 'react';
import { Table, Modal } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';


const ThreadDetails = () => {
  const { url } = useParams();
  const [visible, setVisible] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [dataSource, setDataSource] = useState([]);
  const [ws, setWs] = useState(null);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const decodedUrl = atob(url);
        console.log("url = ", decodedUrl);
        const response = await axios.get(`http://127.0.0.1:8000/get-thread-by-url/?url=${decodedUrl}`);
        const commentsDict = response.data.comments;
        const commentsList = Object.entries(commentsDict).map(([key, value]) => ({ key, ...value }));
        setDataSource(commentsList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [url]);

  useEffect(() => {
    console.log('Connecting to WebSocket');
    const socket = new WebSocket('ws://127.0.0.1:8000/socket-endpoint');
    console.log('Connected to WebSocket',socket);
    setWs(socket);

    socket.addEventListener("message", (event) => {
      console.log("KK socket event = ", event)
      console.log("KK socket event data = ", event.data)
    });

    socket.onmessage = (event) => {
      console.log("socket event = ", event)
      console.log("socket event data = ", event.data)
      const updatedComment = JSON.parse(event.data);
      setDataSource((prevDataSource) =>
        prevDataSource.map((comment) =>
          comment.key === updatedComment.key ? updatedComment : comment
        )
      );
    };

    // socket.onclose = () => {
    //   console.log('WebSocket connection closed');
    // };

    // return () => {
    //   console.log('Closing the WebSocket connection');
    //   socket.close();
    // };
  }, [url]);

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
      title: 'filter',
      dataIndex: 'filter',
      key: 'filter',
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
