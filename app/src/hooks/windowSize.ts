import React from "react";

// Hook
export function useWindowSize() {
  // Initialize state with undefined width/height so server and client renders match
  // Learn more here: https://joshwcomeau.com/react/the-perils-of-rehydration/
  const [windowSize, setWindowSize] = React.useState<{
    width?: number;
    height?: number;
  }>({
    width: undefined,
    height: undefined,
  });

  React.useEffect(() => {
    // only execute all the code below in client side
    if (typeof window !== "undefined") {
      // Add event listener
      window.addEventListener("resize", () => {
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      });

      // Call handler right away so state gets updated with initial window size
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });

      // Remove event listener on cleanup
      return () => window.removeEventListener("resize", () => {
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      });
    }
  }, []); // Empty array ensures that effect is only run on mount
  return windowSize;
}
