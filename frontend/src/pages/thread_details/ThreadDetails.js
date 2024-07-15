import React, { useState, useEffect } from 'react';
import { Table, Modal, Switch, Card } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useSocket } from '../../SocketContext';
import { columns } from './Columns';
import { parseComment } from '../../Utils';
import { remoteWorkColumnRenderer } from '../../components/column_renderers/RemoteWorkAllowed';
import { roleRenderer } from '../../components/column_renderers/Role';
import { contactInfoRenderer } from '../../components/column_renderers/ContactInfo';
import { keyworkRenderer } from '../../components/column_renderers/Keyword';
import { BASE_URL } from '../../Constants';
import { CopyOutlined } from '@ant-design/icons';


const ThreadDetails = () => {
  const { url } = useParams();
  const [visible, setVisible] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [dataSource, setDataSource] = useState([]);
  const [threadDetails, setThreadDetails] = useState({});
  const socket = useSocket();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const decodedUrl = atob(url);
        const response = await axios.get(`${BASE_URL}/get-thread-by-url/?url=${decodedUrl}`);
        const commentsDict = response.data.comments;
        setThreadDetails({
          'title': response.data.title,
          'url': decodedUrl,
        });
        let commentsList = Object.entries(commentsDict).map(([key, value]) => ({ key, ...value }));
        console.log("comments List = ",commentsList)
        commentsList.forEach((comment) =>  parseComment(comment));
        console.log("Parsed comments List = ",commentsList)
        setDataSource(commentsList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [url]);

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        console.log("socket event data = ", event.data)
        const updatedComment = parseComment(JSON.parse(event.data));
        console.log("Updated comment = ", updatedComment)
        setDataSource((dataSource) =>
          dataSource.map((comment) => 
            comment.key === updatedComment.comment_id ? { ...comment,...updatedComment, ...updatedComment.payload }  : comment
          )
        );

      };
    }
  }, [socket]);

  const handleRowClick = (record) => {
    setSelectedRow(record);
    setVisible(true);
  };

  const handleCancel = () => {
    setVisible(false);
    setSelectedRow(null);
  };


  const toggleReadStatus = async (status) => {
    const url = window.location.href.split("/").pop();
    const decodedUrl = atob(url);

    try {
      await axios.post(`${BASE_URL}/update-comment-read-status`, {
        thread_url: decodedUrl,
        comment_id: selectedRow.key,
        is_read: status,
      });
      selectedRow.is_read = status;
    } catch (error) {
      console.error('Error updating read status:', error);
    }
  };

  const copyToClipboard = () => {
    const textToCopy = selectedRow ? selectedRow.GENERATE_COVER_LETTER : '';
    navigator.clipboard.writeText(textToCopy)
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <Card
        style={{ textAlign: 'center', marginBottom: '20px' }}
        title={<h3 style={{ margin: '0', textAlign: 'center' }}>{threadDetails.title} | <a href={threadDetails.url}>{threadDetails.url}</a></h3>}
     >
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        onRow={(record) => ({
          onClick: () => handleRowClick(record),
        })}
      />
      <Modal
        title={
          selectedRow && (
            <div style={{ paddingRight: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <b># {selectedRow.key}</b> {roleRenderer(selectedRow.EXTRACT_ROLES)}
              </div>
              <div>
                <b>Remote :</b> {remoteWorkColumnRenderer(selectedRow.IS_REMOTE_WORK_ALLOWED)}
              </div>
            </div>
          )
        }
        open={visible}
        onCancel={handleCancel}
        onOk={handleCancel}
        footer={[
          <span key={selectedRow && (selectedRow.key+"s")}>Is Read &nbsp;</span>  ,
          <Switch key={selectedRow && selectedRow.key} checked={selectedRow && selectedRow.is_read} onChange={toggleReadStatus} />
        ]}
      >
        {selectedRow && (
          <div>
            <br></br>
            <p>{selectedRow.text}</p>
            {/* <hr></hr> */}
            {keyworkRenderer(selectedRow.EXTRACT_KEYWORDS)}
            <br></br><br></br>
            <p><b>Apply at :</b> {contactInfoRenderer(selectedRow.EXTRACT_CONTACT_INFO)}</p>
            <hr></hr>
            <b>Cover Letter</b>
            <hr></hr>
            <span>{selectedRow.GENERATE_COVER_LETTER}</span><CopyOutlined
              key="copy"
              // icon={<CopyOutlined />}
              onClick={copyToClipboard}
              style={{ marginLeft: '8px' }}
            />
          </div>
        )}
      </Modal>
      </Card>
    </div>
  );
  
};

export default ThreadDetails;
