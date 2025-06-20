"use client";
import { useSimulationContext } from "@/contexts/SimulationContext";
import { FormControl, IconButton, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import ConfigForm from "@/components/ConfigForm";
import { fetchProjectsNames } from "@/lib/fetchers";
import useSWR from "swr";
import { useEffect } from "react";
import { toastError } from "@/hooks/toastError";


export default function DashboardConfiguration() {
    const { data: projectsNames, error: projectsNamesError, isLoading: isLoadingProjectsNames } = useSWR(
        'projects_names', // chave única do cache
        fetchProjectsNames
    );
    const { selectedProject, setSelectedProject } = useSimulationContext();

    const handleSelectProjectChange = (event: SelectChangeEvent<string | null>) => {
        setSelectedProject(event.target.value);
    };

    const handleClearProject = () => {
        setSelectedProject(null);
    };

    const select_project_options = projectsNames?.map((project) => (
        <MenuItem key={project} value={project}>
            {project}
        </MenuItem>
    ));

    let title = selectedProject
        ? <>Configuring project <span className="text-blue-600">{selectedProject}</span></>
        : <>Initialize with <span className="text-blue-600">SnapAI</span> by selecting a project</>;

    if (projectsNamesError) {
        title = <span className="text-red-600">Error loading projects!</span>;
    }

    useEffect(() => {
        if (projectsNamesError) {
            console.error(projectsNamesError);
            toastError('Error loading projects');
        }

    }, [projectsNamesError])

    return (
        <div className="w-full">
            <div style={{ height: '40dvh' }} className="y-spacer"></div>
            <main className="mx-auto max-w-5xl flex flex-col items-center justify-center px-4 ">
                <h1 className="text-5xl font-bold text-gray-900 mb-8 text-center">
                    {title}
                </h1>
                <div className="full-form-container grid-cols-12 grid gap-4 w-full">
                    <div className="select-project-container col-start-3 col-end-11 flex items-center gap-1">
                        <FormControl fullWidth >
                            <InputLabel id="select-project-input-label">Select Project</InputLabel>
                            <Select
                                labelId="select-project-input-label"
                                name="project_name"
                                id="select-project-input"
                                value={selectedProject ?? ""}
                                label="Select Project"
                                onChange={handleSelectProjectChange}
                            >
                                {select_project_options ?? <MenuItem disabled value="" selected>{isLoadingProjectsNames ? 'Loading projects...' : 'Error loading projects'}</MenuItem>}
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
                    <div className="form-container col-start-1 col-end-13">
                        {selectedProject && <ConfigForm project_name={selectedProject} />}
                    </div>
                </div>
            </main>
        </div>
    );
}