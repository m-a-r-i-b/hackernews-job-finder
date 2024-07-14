import React, { useState, useEffect } from 'react';
import { AppstoreOutlined, MailOutlined } from '@ant-design/icons';
import { Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import Threads from './pages/threads/Threads';
import Experience from './pages/experience/Experience';
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
    label: 'My Experience',
    key: 'experience',
    icon: <AppstoreOutlined />,
  }
];

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [current, setCurrent] = useState('threads');

  useEffect(() => {
    const path = location.pathname;
    if (path.startsWith('/thread-details')) {
      setCurrent('');
    } else if (path === '/experience') {
      setCurrent('experience');
    } else {
      setCurrent('threads');
    }
  }, [location]);

  const onClick = (e) => {
    setCurrent(e.key);
    if (e.key === 'threads') {
      navigate('/');
    } else if (e.key === 'experience') {
      navigate('/experience');
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
            <Route path="/thread-details/:url" element={<ThreadDetails />} />
          </Routes>
        </Content>
      </Layout>
    </SocketProvider>
  );
};

export default App;
