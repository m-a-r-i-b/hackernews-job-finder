import React, { useState, useEffect } from 'react';
import { Upload, Button, message, Input } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

const Experience = () => {
  const [file, setFile] = useState(null);
  const [content, setContent] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/get-experience/')
      .then(response => {
        setContent(response.data);
      })
      .catch(error => {
        message.error('Failed to fetch experience.');
      });
  }, []);

  const handleUpload = (info) => {
    if (info.file.status === 'done') {
      const reader = new FileReader();
      reader.onload = (e) => {
        setContent(e.target.result);
      };
      reader.readAsText(info.file.originFileObj);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  };

  const handleSave = () => {
    axios.post('http://127.0.0.1:8000/submit-experience/', {
      experience: content
    })
    .then(response => {
      message.success('Experience saved successfully!');
    })
    .catch(error => {
      message.error('Failed to save experience.');
    });
  };

  const handleChange = (e) => {
    setContent(e.target.value);
  };

  return (
    <div style={{ padding: '20px' }}>
      <Upload onChange={handleUpload} beforeUpload={() => false}>
        <Button icon={<UploadOutlined />}>Select File</Button>
      </Upload>
      <Input.TextArea rows={10} value={content} onChange={handleChange} style={{ marginTop: '20px' }} />
      <Button type="primary" onClick={handleSave} style={{ marginTop: '20px' }}>
        Save
      </Button>
    </div>
  );
};

export default Experience;
