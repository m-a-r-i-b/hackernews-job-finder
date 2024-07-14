import React, { useState, useEffect } from 'react';
import { Upload, Button, message, Input, Spin, Typography } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_URL } from '../../Constants';

const { Title } = Typography;

const Experience = () => {
  const [file, setFile] = useState(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

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

    setLoading(true);  // Set loading state to true

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
    } finally {
      setLoading(false);  // Set loading state to false
    }
  };

  const handleSave = () => {
    setLoading(true);  // Set loading state to true
    axios.post(`${BASE_URL}/submit-experience/`, {
      experience: content
    })
    .then(response => {
      message.success('Experience saved successfully!');
    })
    .catch(error => {
      message.error('Failed to save experience.');
    })
    .finally(() => {
      setLoading(false);  // Set loading state to false
    });
  };

  const handleChange = (e) => {
    setContent(e.target.value);
  };

  return (
    <div style={{ padding: '20px' }}>
      <Title level={3}>Upload resume to extract experience</Title>
      {loading ? <Spin tip="Loading..." /> : ''}
        <>
          <Upload onChange={handleUpload} beforeUpload={() => false}>
            <Button icon={<UploadOutlined />} disabled={loading}>Select File</Button>
          </Upload>
          <Input.TextArea rows={10} value={content} onChange={handleChange} style={{ marginTop: '20px' }} />
          <Button type="primary" onClick={handleSave} style={{ marginTop: '20px' }} disabled={loading}>
            Save
          </Button>
        </>
    </div>
  );
};

export default Experience;
