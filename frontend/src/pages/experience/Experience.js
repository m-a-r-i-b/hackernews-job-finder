import React, { useState, useEffect } from 'react';
import { Upload, Button, message, Input } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_URL } from '../../Constants';

const Experience = () => {
  const [file, setFile] = useState(null);
  const [content, setContent] = useState('');

  useEffect(() => {
    axios.get(`${BASE_URL}/get-experience/`)
      .then(response => {
        setContent(response.data);
      })
      .catch(error => {
        message.error('Failed to fetch experience.');
      });
  }, []);

  const handleUpload = async (options) => {
    const { file } = options;
    setFile(file);  // Set the file state

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BASE_URL}/upload-resume/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setContent(response.data.content);
      message.success(`${file.name} file uploaded successfully.`);
    } catch (error) {
      message.error(`${file.name} file upload failed.`);
    }
  };


  const handleSave = () => {
    axios.post(`${BASE_URL}/submit-experience/`, {
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
