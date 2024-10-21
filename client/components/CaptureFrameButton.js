import React from 'react';

const CaptureFrameButton = ({ captureFrame }) => {
  return (
    <button onClick={captureFrame}>Capture Frame</button>
  );
};

export default CaptureFrameButton;