"use client";
import ControlBar from "@/components/ControlBar";

const data = {
    nodes: [
        { id: 1, fx: 0, fy: 0, fz: 0 }, // Fixo no centro
        { id: 2, fx: 100, fy: 50, fz: -50 }, // Posição fixa personalizada
        { id: 3 }, // Livre (posição calculada pela física)
    ],
    links: [
        { source: 1, target: 2 },
        { source: 2, target: 3 }
    ]
};

export default function DashboardControls() {
    return (
        <div className="flex flex-col w-full justify-center min-h-dvh px-4 col-start-3 col-end-13">
            <ControlBar />
            <div className="flex">
                <div></div>
                <div className="h-full"></div>
            </div>
        </div>
    );
}