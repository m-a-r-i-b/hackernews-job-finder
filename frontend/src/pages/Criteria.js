import React from 'react';
import { Input } from 'antd';

const { TextArea } = Input;

const Criteria = () => {
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h3>Mandatory Criteria</h3>
        <TextArea rows={5} />
      </div>
      <div>
        <h3>Optional Criteria</h3>
        <TextArea rows={5} />
      </div>
    </div>
  );
};

export default Criteria;