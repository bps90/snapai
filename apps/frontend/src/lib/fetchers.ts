import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export type FieldInformative = {
    title: string
    help_text: string
    as_html: boolean
}

export type FieldType = 'text' | 'number' | 'percentage' | 'select' | 'multiselect' | 'checkbox' | 'number_pair' | 'model_select' | 'node_select' | 'color';

export type Field = {
    id: string,
    label: string,
    type: FieldType,
    required: boolean,
    name: string,
    occuped_columns: number,
    informative: FieldInformative | null,
    nested_paths: string[],
    value: unknown,
    afterChange?: (value: unknown) => void;
}

export type Line = {
    fields: Field[]
}

export type Subsection = {
    id: string,
    title: string | null,
    lines: Line[],
    model_parameters: boolean,
}

export type Section = {
    id: string,
    title?: string,
    subsections: Subsection[],
    model?: string,
    model_type?: string,
}

export type Layout = {
    sections: Section[]
}

export type ConfigForm = {
    simulation_name: string,
    simulation_rounds: number,
    simulation_refresh_rate: number,
    nack_messages_enabled: boolean,
    dim_x: [number, number],
    dim_y: [number, number],
    dim_z: [number, number],
    save_trace: boolean,
    asynchronous: boolean,
    connectivity_enabled: boolean,
    message_transmission_model: string,
    message_transmission_model_parameters: Record<string, unknown>,
    project_config: Record<string, unknown>
}

export type GraphData = {
    msg_r: number,
    msg_a: number,
    t: number,
    r: boolean,
    n: [string, number, number, number, number, string][],
    l: [string, string, 0 | 1][],
    logs: string[]
}

export const fetchProjectsNamesDelay = async (): Promise<string[]> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchProjectsNames().then(resolve).catch(reject)
        }, 1500);
    })
}

export const fetchProjectsNames = async (): Promise<string[]> => {
    const response = await axios.get<string[]>(`${API_BASE_URL}/graph/projects_names/`);
    return response.data;
};

export const fetchConfigFormLayoutDelay = (project: string): Promise<{ simulation_config_layout: Layout; project_config_layout: Layout | null }> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchConfigFormLayout(project).then(resolve).catch(reject);
        }, 1500)
    })
}

export const fetchConfigFormLayout = async (
    project: string
): Promise<{ simulation_config_layout: Layout; project_config_layout: Layout | null }> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_config_form_layout/`, {
        params: { project },
    });
    return response.data;
};

export const fetchConfigFormDelay = (project: string): Promise<ConfigForm> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchConfigForm(project).then(resolve).catch(reject);
        }, 3000)
    })
}

export const fetchConfigForm = async (project: string): Promise<ConfigForm> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_config/`, {
        params: { project },
    });
    return response.data;
};

export const fetchModelSubsectionLayoutDelay = (model: string, model_type: string): Promise<Subsection> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchModelSubsectionLayout(model, model_type).then(resolve).catch(reject);
        }, 1500)
    })
}

export const fetchModelSubsectionLayout = async (
    model: string,
    model_type: string,
): Promise<Subsection> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_model_subsection_layout/`, {
        params: { model, model_type },
    });
    return response.data;
}

export const updateConfig = async (project: string, data: Record<string, unknown>): Promise<void> => {
    await axios.post(`${API_BASE_URL}/graph/update_config/`, {
        ...data
    }, {
        params: {
            project
        }
    });
}

export const getData = async (withLogs: boolean): Promise<GraphData> => {
    const response = await axios.get(`${API_BASE_URL}/graph/update_graph/`, {
        params: { with_logs: withLogs },
    });
    return response.data;
}

export const initSimulation = async (project: string): Promise<void> => {
    await axios.post(`${API_BASE_URL}/graph/init_simulation/`, {}, {
        params: { project },
    });
}

export const fetchNodeSubsectionLayout = async (
    node: string,
): Promise<{ layout: Subsection, defaultParameters: boolean }> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_node_subsection_layout/`, {
        params: { node },
    });
    return response.data;
}

export const fetchNodesNames = async (): Promise<string[]> => {
    const response = await axios.get<string[]>(`${API_BASE_URL}/graph/get_nodes_names/`);
    return response.data;
}

export const fetchModelsNames = async (modelType: string): Promise<string[]> => {
    const response = await axios.get<string[]>(`${API_BASE_URL}/graph/get_models_names/`, {
        params: { model_type: modelType }
    });
    return response.data;
}