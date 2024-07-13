import React, { useState } from 'react';
import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';
import { Route, Routes, useNavigate } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import Threads from './pages/threads/Threads';
import Experience from './pages/experience/Experience';
import Criteria from './pages/criteria/Criteria';
import ThreadDetails from './pages/thread_details/ThreadDetails';
import { SocketProvider } from './SocketContext';

const { Header, Content } = Layout;

const items = [
  {
    label: 'Threads',
    key: 'threads',
    icon: <MailOutlined />,
  },
  {
    label: 'Experience',
    key: 'experience',
    icon: <AppstoreOutlined />,
  },
  {
    label: 'Criteria',
    key: 'criteria',
    icon: <SettingOutlined />,
  }
];

const App = () => {
  const [current, setCurrent] = useState('threads');
  const navigate = useNavigate();

  const onClick = (e) => {
    console.log('click ', e);
    setCurrent(e.key);

    if (e.key === 'threads') {
      navigate('/');
    } else if (e.key === 'experience') {
      navigate('/experience');
    } else if (e.key === 'criteria') {
      navigate('/criteria');
    }
  };

  return (
    <SocketProvider>
      <Layout>
        <Header style={{ padding: '0px' }}>
          <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
        </Header>
        <Content style={{ padding: '20px' }}>
          <Routes>
            <Route path="/" element={<Threads />} />
            <Route path="/experience" element={<Experience />} />
            <Route path="/criteria" element={<Criteria />} />
            <Route path="/thread-details/:url" element={<ThreadDetails />} />
          </Routes>
        </Content>
      </Layout>
    </SocketProvider>
  );
};

export default App;
