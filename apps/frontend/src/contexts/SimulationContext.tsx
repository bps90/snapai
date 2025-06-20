"use client";
import React, { createContext, useState, useContext } from 'react';

type SimulationContextProps = {
    selectedProject: string | null;
    setSelectedProject: React.Dispatch<React.SetStateAction<string | null>>;
}

const SimulationContext = createContext<SimulationContextProps | undefined>(undefined);

type SimulationProviderProps = {
    children: React.ReactNode;
}

export const SimulationProvider = ({ children }: SimulationProviderProps) => {
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
