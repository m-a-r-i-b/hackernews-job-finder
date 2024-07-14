import React, { useState, useEffect } from 'react';
import { Card, Button, Modal, Form, Input, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BASE_URL } from '../../Constants';

const Threads = () => {
  const navigate = useNavigate();
  const [threads, setThreads] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [title, setTitle] = useState('');
  const [url, setUrl] = useState('https://news.ycombinator.com/item?id=40224213');
  const [loading, setLoading] = useState(false);

  const fetchThreads = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/get-threads/`);
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
    if (!/^https:\/\/news\.ycombinator\.com\/item\?id=\d+$/.test(url)) {
      message.error('URL must be in the format: https://news.ycombinator.com/item?id=40224213');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${BASE_URL}/submit-thread/`, {
        title: title,
        url: url
      });
      console.log('Thread added successfully:', response.data);

      message.success('Thread added successfully!');
      setModalVisible(false);
      fetchThreads();
      navigateToDetailsPage(url);
    } catch (error) {
      console.error('Error adding thread:', error);
      message.error('Error adding thread. Please try again.');
    } finally {
      setLoading(false);
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
        open={modalVisible}
        onOk={handleAddThread}
        onCancel={handleModalClose}
        confirmLoading={loading}
        okButtonProps={{ disabled: loading }}
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
