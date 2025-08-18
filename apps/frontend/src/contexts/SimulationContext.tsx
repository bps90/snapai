"use client";
import { GraphData } from '@/components/GraphViewer';
import React, { createContext, useState, useContext } from 'react';
import { CameraState } from 'sigma/types';

export type SimulationContextProps = {
    selectedProject: string | null;
    setSelectedProject: React.Dispatch<React.SetStateAction<string | null>>;
    showArrows: boolean;
    setShowArrows: React.Dispatch<React.SetStateAction<boolean>>;
    showIds: boolean;
    setShowIds: React.Dispatch<React.SetStateAction<boolean>>;
    mouseInNode: string | null;
    setMouseInNode: React.Dispatch<React.SetStateAction<string | null>>;
    graphData: GraphData;
    setGraphData: React.Dispatch<React.SetStateAction<GraphData>>;
    cameraState: CameraState | null;
    setCameraState: React.Dispatch<React.SetStateAction<CameraState | null>>;
    isRunning: boolean;
    setIsRunning: React.Dispatch<React.SetStateAction<boolean>>;
}

const SimulationContext = createContext<SimulationContextProps | undefined>(undefined);

type SimulationProviderProps = {
    children: React.ReactNode;
}

export const SimulationProvider = ({ children }: SimulationProviderProps) => {
    const [selectedProject, setSelectedProject] = useState<string | null>(null);
    const [showArrows, setShowArrows] = useState(true);
    const [showIds, setShowIds] = useState(true);
    const [mouseInNode, setMouseInNode] = useState<string | null>(null);
    const [graphData, setGraphData] = useState<GraphData>({
        links: [],
        nodes: [],
    });
    const [cameraState, setCameraState] = useState<CameraState | null>(null);
    const [isRunning, setIsRunning] = useState(false);

    return (
        <SimulationContext.Provider value={{
            selectedProject, setSelectedProject,
            showArrows, setShowArrows,
            showIds, setShowIds,
            mouseInNode, setMouseInNode,
            graphData, setGraphData,
            cameraState, setCameraState,
            isRunning, setIsRunning
        }}>
            {children}
        </SimulationContext.Provider>
    );
};

export const useSimulationContext = (): SimulationContextProps => {
    const context = useContext(SimulationContext);
    if (!context) {
        throw new Error('useSimulationContext must be used within a SimulationProvider');
    }
    return context;
};
