"use client";
import { AddNodesFormSchema } from '@/components/form/AddNodesForm';
import { GraphData } from '@/components/GraphViewer';
import { zodResolver } from '@hookform/resolvers/zod';
import { useQueryState } from 'nuqs';
import React, { createContext, useState, useContext } from 'react';
import { useForm, UseFormReturn } from 'react-hook-form';
import { CameraState } from 'sigma/types';
import { z } from 'zod';

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
    logs: string[];
    setLogs: React.Dispatch<React.SetStateAction<string[]>>;
    time: number;
    setTime: React.Dispatch<React.SetStateAction<number>>;
    numberOfMessagesInThisRound: number;
    setNumberOfMessagesInThisRound: React.Dispatch<React.SetStateAction<number>>;
    numberOfMessagesOverAll: number;
    setNumberOfMessagesOverAll: React.Dispatch<React.SetStateAction<number>>;
    dimensions: { x: [number, number]; y: [number, number]; };
    setDimensions: React.Dispatch<React.SetStateAction<{ x: [number, number]; y: [number, number]; }>>;
}

const SimulationContext = createContext<SimulationContextProps | undefined>(undefined);

type SimulationProviderProps = {
    children: React.ReactNode;
}

export const SimulationProvider = ({ children }: SimulationProviderProps) => {
    const [selectedProject, setSelectedProject] = useQueryState<string | null>('project', { defaultValue: null, parse: (s) => s ? s : null });
    const [showArrows, setShowArrows] = useQueryState('showArrows', {
        defaultValue: true,
        parse: (s) => s === 'true',
    });
    const [showIds, setShowIds] = useQueryState('showIds', {
        defaultValue: true,
        parse: (s) => s === 'true',
    });
    const [mouseInNode, setMouseInNode] = useState<string | null>(null);
    const [graphData, setGraphData] = useState<GraphData>({
        links: [],
        nodes: [],
    });
    const [cameraState, setCameraState] = useState<CameraState | null>(null);
    const [isRunning, setIsRunning] = useState(false);
    const [logs, setLogs] = useState<string[]>([]);
    const [time, setTime] = useState(0);
    const [numberOfMessagesInThisRound, setNumberOfMessagesInThisRound] = useState(0);
    const [numberOfMessagesOverAll, setNumberOfMessagesOverAll] = useState(0);
    const [dimensions, setDimensions] = useState<{ x: [number, number]; y: [number, number]; }>({ x: [0, 0], y: [0, 0] });

    return (
        <SimulationContext.Provider value={{
            selectedProject, setSelectedProject,
            showArrows, setShowArrows,
            showIds, setShowIds,
            mouseInNode, setMouseInNode,
            graphData, setGraphData,
            cameraState, setCameraState,
            isRunning, setIsRunning,
            logs, setLogs,
            time, setTime,
            numberOfMessagesInThisRound, setNumberOfMessagesInThisRound,
            numberOfMessagesOverAll, setNumberOfMessagesOverAll,
            dimensions, setDimensions
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
