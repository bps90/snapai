"use client";
import React, { createContext, useState, useContext } from 'react';

interface SimulationContextProps {
    selectedProject: string | null;
    setSelectedProject: React.Dispatch<React.SetStateAction<string | null>>;
}

const SimulationContext = createContext<SimulationContextProps | undefined>(undefined);

interface ISimulationProviderProps {
    children: React.ReactNode;
}

export const SimulationProvider = ({ children }: ISimulationProviderProps) => {
    const [selectedProject, setSelectedProject] = useState<string | null>(null);

    return (
        <SimulationContext.Provider value={{ selectedProject, setSelectedProject }}>
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
