// Camera.js
import React, { useRef, useEffect } from 'react';

const Camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const getVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing the camera: ", err);
      }
    };

    getVideo();
  }, [videoRef]);

  const captureFrame = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (canvas && video) {
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/png');
      // Send dataUrl to the back-end
      fetch('http://localhost:8080/api/process_frame', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataUrl }),
      });
    }
  };

  return (
    <div>
      <video ref={videoRef} autoPlay style={{ width: '100%' }} />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <button onClick={captureFrame}>Capture Frame</button>
    </div>
  );
};

export default Camera;