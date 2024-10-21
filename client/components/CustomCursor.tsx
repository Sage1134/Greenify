import { useEffect, useRef } from "react";
import { gsap } from "gsap";

const CustomCursor = () => {
  const cursorRef = useRef<HTMLDivElement>(null);
  const backgroundRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    const background = backgroundRef.current || document.body; // Apply unblur to the body

    if (!cursor || !background) return;

    const cursorXTo = gsap.quickTo(cursor, "left", { duration: 0.2, ease: "power3" });
    const cursorYTo = gsap.quickTo(cursor, "top", { duration: 0.2, ease: "power3" });

    const moveCursor = (e: MouseEvent) => {
      const mouseX = e.clientX;
      const mouseY = e.clientY;

      // Move the custom cursor
      cursorXTo(mouseX - 25); // Adjust for cursor center
      cursorYTo(mouseY - 25);

      // Create unblur effect around cursor
      const clipPathValue = `circle(100px at ${mouseX}px ${mouseY}px)`;
      background.style.clipPath = clipPathValue;
    };

    document.addEventListener("mousemove", moveCursor);

    return () => {
      document.removeEventListener("mousemove", moveCursor);
    };
  }, []);

  return (
    <div className="pageWrapper">
      <div ref={cursorRef} className='customCursor'></div>
    </div>
  );
};

export default CustomCursor;