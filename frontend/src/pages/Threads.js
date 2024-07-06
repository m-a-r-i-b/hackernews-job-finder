import React from 'react';
import { Card, Button } from 'antd';
import { useNavigate } from 'react-router-dom';

const Threads = () => {

  const navigate = useNavigate();
  const threads = [
    { title: 'Thread 1', content: 'This is thread 1' },
    { title: 'Thread 2', content: 'This is thread 2' },
  ];

  const handleCardClick = (id) => {
    navigate(`/thread-details/${id}`);
  };

  return (
    <div style={{ padding: '20px', display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
      {threads.map((thread, index) => (
        <Card title={thread.title} key={index} style={{ width: 300 }} onClick={() => handleCardClick(thread.title)}>
          <p>{thread.content}</p>
        </Card>
      ))}
      <Card style={{ width: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Button type="primary">Create New Thread</Button>
      </Card>
    </div>
  );
};

export default Threads;