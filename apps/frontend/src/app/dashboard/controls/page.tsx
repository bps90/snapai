"use client";

import dynamic from "next/dynamic";
import ControlBar from "@/components/ControlBar";

// Importa sem SSR
const GraphViewer = dynamic(() => import("@/components/GraphViewer"), { ssr: false });

export default function DashboardControls() {
    return (
        <div className="flex flex-col w-full justify-center min-h-dvh px-4 col-start-3 col-end-13">
            <ControlBar />
            <div className="flex" >
                <GraphViewer />
            </div>
        </div>
    );
}
