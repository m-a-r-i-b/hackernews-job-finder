import React, { useState } from 'react';
import { Upload, Button, message, Input } from 'antd';
import { UploadOutlined } from '@ant-design/icons';


const Experience = () => {
  const [file, setFile] = useState(null);
  const [content, setContent] = useState('');

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

  return (
    <div style={{ padding: '20px' }}>
      <Upload onChange={handleUpload} beforeUpload={() => false}>
        <Button icon={<UploadOutlined />}>Select File</Button>
      </Upload>
      <Input.TextArea rows={10} value={content} readOnly style={{ marginTop: '20px' }} />
    </div>
  );
};

export default Experience;