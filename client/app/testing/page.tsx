'use client'

import Image from "next/image";
import React, {useEffect, useState} from 'react';
import Camera from '@/components/Camera'

export default function Page() {

  const [message, setMessage] = useState("Loading");
  const [cameraEnabled, setCameraEnabled] = useState(true);
 

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
    .then((response) => response.json())
    .then((data) => {
3
      setMessage("Loaded");

      console.log(data)
    })
  }, [])

  const toggleCamera = () => {
    setCameraEnabled(!cameraEnabled);
  }
  return (
    <main className='bg-black min-h-screen'>
      <div className='bg-noise text-white min-h-screen'>
        <div className='blur-noise min-h-screen flex justify-center items-center w-full'>


          <section className='grid grid-cols-3 justify-center items-center mx-20'>
            <div className='flex flex-col col-span-2 justify-start items-start gap-y-6 w-full'>
              <div className='w-[750px] h-[689px] box-1 justify-center items-center flex flex-col gap-y-16'>
                <div className="w-[653px] h-[519px] rounded-xl flex justify-center items-center">
                  {cameraEnabled && <Camera />}
                </div>
              </div>
              <div className='box-2 w-[750px] h-[87px]'>
              </div>
            </div>
            <div className='flex justify-center items-center'>
              <div className='box-3 w-[486px] h-[800px]'>

              </div>
            </div>
          </section>


        </div>
      </div>
    </main>
  )
}