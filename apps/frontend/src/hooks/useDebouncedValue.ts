import { useState, useEffect } from "react";

export function useDebouncedValue(value: unknown, delay = 500) {
    console.log('value');
    const [debounced, setDebounced] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(handler);
    }, [value, delay]);

    return debounced;
}