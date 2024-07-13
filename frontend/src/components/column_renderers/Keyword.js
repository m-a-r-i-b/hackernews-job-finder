import BlinkingDot from '../../components/blinking_dot/BlinkingDot';
import ProcessingDot from '../../components/processing_dot/ProcessingDot';
import { Tag } from 'antd';
import { assignColorToKeyword } from '../../Utils';


export function keyworkRenderer(keywords) {
    if (keywords === '-') {
      return keywords;
    }
    if (keywords === 'PROCESSING') {
      return <ProcessingDot />;
    }
    if (!keywords) {
      return <BlinkingDot />;
    }
    return keywords.split(',').map((keyword, index) => {
      const trimmedKeyword = keyword.trim().toLowerCase();
      let languageColor = assignColorToKeyword(trimmedKeyword);

      return (
        <Tag key={index} color={languageColor || 'default'}>
          {keyword.trim()}
        </Tag>
      );
    });
}