import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export type FieldInformative = {
    title: string
    help_text: string
    as_html: boolean
}

export type FieldType = 'text' | 'number' | 'percentage' | 'select' | 'multiselect' | 'checkbox' | 'number_pair' | 'model_select';

export type Field = {
    id: string,
    label: string,
    type: FieldType,
    required: boolean,
    name: string,
    occuped_columns: number,
    informative: FieldInformative | null,
    nested_paths: string[],
    value: unknown
}

export type Line = {
    fields: Field[]
}

export type Subsection = {
    id: string,
    title: string | null,
    lines: Line[]
}

export type Section = {
    id: string,
    title: string,
    subsections: Subsection[]
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

export const fetchProjectsNames = async (): Promise<string[]> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchProjectsNamesOri().then(resolve).catch(reject)
        }, 1500);
    })
}

export const fetchProjectsNamesOri = async (): Promise<string[]> => {
    const response = await axios.get<string[]>(`${API_BASE_URL}/graph/projects_names/`);
    return response.data;
};

export const fetchConfigFormLayout = (project: string): Promise<{ simulation_config_layout: Layout; project_config_layout: Layout | null }> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchConfigFormLayoutOri(project).then(resolve).catch(reject);
        }, 1500)
    })
}

export const fetchConfigFormLayoutOri = async (
    project: string
): Promise<{ simulation_config_layout: Layout; project_config_layout: Layout | null }> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_config_form_layout/`, {
        params: { project },
    });
    return response.data;
};

export const fetchConfigForm = (project: string): Promise<ConfigForm> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            fetchConfigFormOri(project).then(resolve).catch(reject);
        }, 3000)
    })
}



export const fetchConfigFormOri = async (project: string): Promise<ConfigForm> => {
    const response = await axios.get(`${API_BASE_URL}/graph/get_config/`, {
        params: { project },
    });
    return response.data;
};