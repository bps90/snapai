import { useEffect, useState } from "react";

export type LogsProps = {
    logs: string[];
}

const Logs = ({ logs }: LogsProps) => {
    return (
        <pre className="styled-scrollbar flex gap-1.5 flex-col overflow-y-scroll bg-gray-800 rounded-md p-2 border-gray-600 h-full border text-gray-200 font-mono text-sm">
            {logs.toReversed().map((log, index) => (
                <p key={index} className="pl-1.5 border-l-2 border-gray-600">{log}</p>
            ))}
        </pre>
    )
}

export default Logs