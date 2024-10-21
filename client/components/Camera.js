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
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'capture.png');

        try {
          const response = await fetch('http://localhost:8080/api/process_frame', {
            method: 'POST',
            body: formData,
          });

          // Check if response is OK
          if (!response.ok) {
            const errorText = await response.text();
            console.error("Error response from server:", errorText);
            throw new Error(errorText);
          }

          const result = await response.json(); // Parse the JSON response
          console.log("Response from server:", result); // Log the result to the console
        } catch (error) {
          console.error("Error sending image to backend:", error);
        }
      }, 'image/png');
    }
  };

  return (
    <div>
      <video ref={videoRef} className='rounded-xl ' autoPlay style={{ width: '100%' }} />
      <canvas ref={canvasRef} className='rounded-xl ' style={{ display: 'none' }} />
      <button onClick={captureFrame}>Capture Frame</button>
    </div>
  );
};

export default Camera;
