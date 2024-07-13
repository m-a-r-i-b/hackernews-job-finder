import BlinkingDot from '../../components/blinking_dot/BlinkingDot';
import ProcessingDot from '../../components/processing_dot/ProcessingDot';


export function contactInfoRenderer(value) {
    if (value === 'PROCESSING') {
      return <ProcessingDot />;
    }
    return value === undefined ? <BlinkingDot /> : value;
}