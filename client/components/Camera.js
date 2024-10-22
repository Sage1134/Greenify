import React, { useRef, useEffect, useState } from 'react';

const Camera = () => {
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [resultData, setResultData] = useState(null);
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

          if (!response.ok) {
            const errorText = await response.text();
            console.error("Error response from server:", errorText);
            throw new Error(errorText);
          }

          const result = await response.json();
          console.log("Response from server:", result);

          if (result.detected_classes.length === 0 && result.advice.length === 0) {
            setResultData({
              detected_classes: ["All green!"],
              advice: [""]
            });
          } else {
            setResultData({
              detected_classes: result.detected_classes,
              advice: result.advice
            });
          }

          setIsPopupVisible(true);

        } catch (error) {
          console.error("Error sending image to backend:", error);
        }
      }, 'image/png');
    }
  };

  const togglePopup = () => {
    setIsPopupVisible(!isPopupVisible);
  };

  return (
    <div className='z-50'>
      <video ref={videoRef} className='rounded-xl ' autoPlay style={{ width: '100%' }} />
      <canvas ref={canvasRef} className='rounded-xl' style={{ display: 'none' }} />
      <button onClick={captureFrame} className="relative bg-black p-4 rounded-full w-full text-4xl mt-8 flex justify-center items-center text-center text-white hover:bg-gray-800 active:bg-gray-700 transition-all duration-300 transform active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
        Click!
        <span className="absolute inset-0 bg-gray-600 opacity-0 transition-opacity duration-300 ease-in-out group-active:opacity-25"></span>
      </button>
      {isPopupVisible && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center'>
          <div className='bg-white p-8 rounded-lg mx-80'>
            <h2 className='text-2xl mb-4 text-black'>Feedback</h2>
            {resultData && (
              <div className='text-black mb-4'>
                {resultData.detected_classes[0] === "All green!" ? (
                  <strong>Nice job in choosing to go green! Well done!</strong>
                ) : (
                  resultData.detected_classes.map((topic, index) => (
                    <div key={index}>
                      <strong>{topic}</strong> - {resultData.advice[index]}
                    </div>
                  ))
                )}
              </div>
            )}
            <button onClick={togglePopup} className='bg-red-500 text-white p-2 rounded'>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Camera;
