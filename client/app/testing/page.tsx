'use client'

import React, { useState } from 'react';
import Camera from '@/components/Camera';
import CustomCursor from "@/components/CustomCursor";

interface ApiResponse {
  detected_classes: string[];
  advice: string[];
}

export default function Page() {
  const [detectedClasses, setDetectedClasses] = useState<string[]>([]);
  const [advice, setAdvice] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showMessage, setShowMessage] = useState(false);

  const handleTextClick = () => {
    setShowMessage(true);
  };

  // Function to send image to /api/process_frame
  const processImage = async (photoBlob: Blob) => {
    const formData = new FormData();
    formData.append('image', photoBlob, 'photo.png'); // Assuming photoBlob is the captured photo

    try {
      setIsLoading(true);
      const response = await fetch('/api/process_frame', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error processing the image');
      }

      const data: ApiResponse = await response.json();
      setDetectedClasses(data.detected_classes);
      setAdvice(data.advice);
      setError(null); // Clear any previous errors
    } catch (err) {
      setError('An error occurred while processing the image.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // This is a placeholder for triggering the photo capture and image processing
  const handleTakePhoto = async () => {
    const photoBlob = await capturePhoto(); // Replace with your camera logic to get the image as a Blob
    await processImage(photoBlob); // Process the captured photo
  };

  // Simulate capturing a photo (replace this with actual camera logic)
  const capturePhoto = async (): Promise<Blob> => {
    // Your photo capturing logic goes here
    return new Blob(); // Replace this with actual photo Blob/File from the camera
  };

  return (
    <main className='bg-black min-h-screen'>

      <div className='blurredBackground absolute inset-0 min-h-screen waveBlurEffect z-0'></div>
     
        <div className='min-h-screen absolute flex justify-center items-center w-full z-50 text-white'>
          <section className='grid grid-cols-3 justify-center items-center mx-20 z-50'>
            <div className='flex flex-col col-span-3 justify-start items-start gap-y-6 w-full z-50'>
              <div className='w-[750px] h-[689px] box-1 justify-center items-center flex flex-col gap-y-16 z-50'>
                <div className="w-[653px] h-[519px] rounded-xl flex flex-col justify-center items-center z-50 gap-y-6">

                  <p className='text-5xl text-bold coolText'>Greenify</p>
                  <Camera /> 
                </div>
              </div>
            </div>
          </section>
        </div>
    </main>
  );
}