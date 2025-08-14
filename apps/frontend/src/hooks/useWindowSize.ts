"use client";
import { useState, useEffect } from "react";

export function useWindowSize() {
    const [size, setSize] = useState({
        width: global.window ? window.innerWidth : 0,
        height: global.window ? window.innerHeight : 0
    });

    useEffect(() => {
        function handleResize() {
            setSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        }

        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return size;
}
