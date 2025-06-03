"use client";
import { useSimulationContext } from "@/contexts/SimulationContext";
import { FormControl, IconButton, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { useEffect, useState } from "react";
import CloseIcon from '@mui/icons-material/Close';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function DashboardConfiguration() {
    const [projects, setProjects] = useState<string[]>([]);
    const { selectedProject, setSelectedProject } = useSimulationContext();

    const fetchProjects = async () => {
        try {
            const response = await fetch(API_BASE_URL + '/graph/projects_names');
            const data = await response.json();
            setProjects(data);
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
    };

    useEffect(() => {
        fetchProjects();
    }, []);

    const handleSelectProjectChange = (event: SelectChangeEvent<string | null>) => {
        setSelectedProject(event.target.value);
    };

    const handleClearProject = () => {
        setSelectedProject(null);
    };

    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4 col-start-3 col-end-13">
            <h1 className="text-5xl font-bold text-gray-900 mb-8 text-center">
                {!selectedProject
                    ? <>Initialize with <span className="text-blue-600">SnapAI</span> by selecting a project</>
                    : <><span className="text-blue-600">{selectedProject}</span></>}
            </h1>

            <div className="form grid-cols-12 grid gap-4 w-full">
                <div className="col-start-3 col-end-11 flex items-center gap-1">
                    <FormControl fullWidth >
                        <InputLabel id="select-project-input-label">Select Project</InputLabel>
                        <Select
                            labelId="select-project-input-label"
                            id="select-project-input"
                            value={selectedProject ?? ""}
                            label="Select Project"
                            onChange={handleSelectProjectChange}
                        >
                            {projects.map((project) => (
                                <MenuItem key={project} value={project}>
                                    {project}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {selectedProject && (
                        <IconButton
                            aria-label="Clear selection"
                            onClick={handleClearProject}
                            size="small"
                            className="mt-2"
                        >
                            <CloseIcon fontSize="small" />
                        </IconButton>
                    )}
                </div>
            </div>

        </main>
    );
}