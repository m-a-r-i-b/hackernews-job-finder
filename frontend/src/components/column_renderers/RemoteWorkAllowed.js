import BlinkingDot from '../../components/blinking_dot/BlinkingDot';
import ProcessingDot from '../../components/processing_dot/ProcessingDot';
import { Tag } from 'antd';


export function remoteWorkColumnRenderer(value) {
    if (value === 'PROCESSING') {
      return <ProcessingDot />;
    }
    if (value === undefined || value === null) {
      return <BlinkingDot />;
    }
    return (
      <Tag color={value === 'true' ? 'green' : 'red'}>
        {value === 'true' ? 'YES' : 'NO'}
      </Tag>
    );
}