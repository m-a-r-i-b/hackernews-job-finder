import React, { useState, useEffect } from 'react';
import { Card, Button, Modal, Form, Input } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Threads = () => {
  const navigate = useNavigate();
  const [threads, setThreads] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [title, setTitle] = useState('');
  const [url, setUrl] = useState('');

  const fetchThreads = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/get-threads/');
      setThreads(response.data);
      console.log("threads", response.data);
    } catch (error) {
      console.error('Error fetching threads:', error);
    }
  };

  useEffect(() => {
    fetchThreads();
  }, []);

  const navigateToDetailsPage = (url) => {
    navigate(`/thread-details/${btoa(url)}`);
  };

  const handleModalOpen = () => {
    setModalVisible(true);
  };

  const handleModalClose = () => {
    setModalVisible(false);
  };

  const handleAddThread = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/submit-thread/', {
        title: title,
        url: url
      });
      console.log('Thread added successfully:', response.data);

      setModalVisible(false);
      fetchThreads();
      navigateToDetailsPage(url)
    } catch (error) {
      console.error('Error adding thread:', error);
    }
  };

  return (
    <div style={{ padding: '20px', display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
      {threads.map((thread, index) => (
        <Card title={thread.title} key={index} style={{ width: 300 }} onClick={() => navigateToDetailsPage(thread.url)}>
          <p>count: {thread.comment_count}</p>
          <p>url: {thread.url}</p>
        </Card>
      ))}
      <Card style={{ width: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Button type="primary" onClick={handleModalOpen}>Create New Thread</Button>
      </Card>

      <Modal
        title="Create New Thread"
        visible={modalVisible}
        onOk={handleAddThread}
        onCancel={handleModalClose}
      >
        <Form layout="vertical">
          <Form.Item label="Title">
            <Input value={title} onChange={(e) => setTitle(e.target.value)} />
          </Form.Item>
          <Form.Item label="URL">
            <Input value={url} onChange={(e) => setUrl(e.target.value)} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Threads;
