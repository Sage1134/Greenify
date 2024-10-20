'use client';

import React, { useEffect, useState, useRef } from 'react';

export default function Page() {
    const [message, setMessage] = useState("Loading...");
    const [cameraEnabled, setCameraEnabled] = useState(true);
    const [advice, setAdvice] = useState([]);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    useEffect(() => {
        fetch("http://localhost:8080/api/home")
            .then((response) => response.json())
            .then((data) => {
                setMessage("Loaded");
                console.log(data);
            });
    }, []);

    const toggleCamera = () => {
        setCameraEnabled(!cameraEnabled);
    };

    const captureImage = () => {
        const canvas = canvasRef.current;
        const video = videoRef.current;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);

        // Convert the canvas to a base64 image
        const imageData = canvas.toDataURL('image/png');
        sendToBackend(imageData);
    };

    const sendToBackend = async (imageData) => {
        try {
            const response = await fetch("http://localhost:8080/api/process_frame", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData }),
            });

            const data = await response.json();
            console.log(data);
            setAdvice(data.advice);
        } catch (error) {
            console.error("Error sending image to backend:", error);
        }
    };

    return (
        <main className='bg-black min-h-screen'>
            <div className='bg-noise text-white min-h-screen'>
                <div className='blur-noise min-h-screen flex justify-center items-center w-full'>
                    <section className='grid grid-cols-3 justify-center items-center mx-20'>
                        <div className='flex flex-col col-span-2 justify-start items-start gap-y-6 w-full'>
                            <div className='w-[750px] h-[726px] box-1 justify-center items-center flex flex-col gap-y-16'>
                                <p className="text-5xl text-white font-light">{message}</p>
                                <div className="w-[653px] h-[519px] rounded-xl">
                                    {cameraEnabled && (
                                        <div>
                                            <video ref={videoRef} autoPlay playsInline className="rounded-xl" />
                                            <canvas ref={canvasRef} style={{ display: 'none' }} />
                                            <button onClick={captureImage} className="mt-4 bg-blue-500 text-white p-2 rounded">
                                                Capture Image
                                            </button>
                                        </div>
                                    )}
                                </div>
                                <div className="advice-box">
                                    {advice.length > 0 && (
                                        <div>
                                            <h2 className="text-2xl text-white">Advice:</h2>
                                            <ul className="text-white">
                                                {advice.map((item, index) => (
                                                    <li key={index}>{item}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            </div>
                            <div className='box-2 w-[750px] h-[87px]'></div>
                        </div>
                        <div className='flex justify-center items-center'>
                            <div className='box-3 w-[486px] h-[837px]'></div>
                        </div>
                    </section>
                </div>
            </div>
            <style jsx>{`
                video {
                    width: 100%;
                    height: auto;
                    border-radius: 12px;
                }
            `}</style>
        </main>
    );
}
