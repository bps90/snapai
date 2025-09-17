import { useRef, useEffect } from "react";

export default function useWhyDidYouRender(name: string, props: Record<string, unknown>) {
    const prevProps = useRef(props);

    useEffect(() => {
        const changedProps: Record<string, unknown> = {};
        for (const key in props) {
            if (props[key] !== prevProps.current[key]) {
                changedProps[key] = { from: prevProps.current[key], to: props[key] };
            }
        }

        if (Object.keys(changedProps).length > 0) {
            console.log("[why-did-you-render]", name, changedProps);
        } else {
            console.log("[why-did-you-render]", name, "changedProp is not in props");
        }

        prevProps.current = props;
    });
}

