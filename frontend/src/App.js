import React from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import Threads from './pages/Threads';
import Experience from './pages/Experience';
import Criteria from './pages/Criteria';
import ThreadDetails from './pages/ThreadDetails';

const { Header, Content } = Layout;

const App = () => {
  return (
    <Layout>
      <Header>
        <Menu theme="dark" mode="horizontal">
          <Menu.Item key="1">
            <Link to="/">Threads</Link>
          </Menu.Item>
          <Menu.Item key="2">
            <Link to="/experience">Experience</Link>
          </Menu.Item>
          <Menu.Item key="3">
            <Link to="/criteria">Criteria</Link>
          </Menu.Item>
        </Menu>
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
  );
};

export default App;
