/* eslint-disable @typescript-eslint/no-explicit-any */
import { toastError } from "@/hooks/toastError";
import { fetchConfigForm, fetchConfigFormLayout, fetchModelSubsectionLayout, Layout, Section as SectionType, Subsection, updateConfig } from "@/lib/fetchers";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import useSWR from "swr";
import { z } from 'zod'
import clsx from 'clsx'
import Section from "./formDivisions/Section";
import { TextField } from "./fields/TextField";
import { NumberField } from "./fields/NumberField";
import { CheckboxField } from "./fields/CheckboxField";
import { MultiSelectField } from "./fields/MultiSelectField";
import { useErrorModal } from "@/contexts/ErrorModalContext";
import dynamic from 'next/dynamic';
import { toast } from "sonner";

const ReactJson = dynamic(() => import('react-json-view'), { ssr: false });

type SchemaBuilderLayout = Layout & { nestedPaths?: string[] }

function buildSchema(layouts: SchemaBuilderLayout[]) {
    const schema: Record<string, z.ZodType> = {};

    for (const layout of layouts) {
        for (const section of layout.sections) {
            for (const subsection of section.subsections) {
                for (const line of subsection.lines) {
                    for (const field of line.fields) {
                        let base: z.ZodType;

                        switch (field.type) {
                            case 'text':
                                base = z.string().min((field as TextField).min_length).max((field as TextField).max_length || Infinity);
                                break;
                            case 'number':
                                base = ((field as NumberField).is_float ? z.number() : z.number().int()).min((field as NumberField).min_value || -Infinity).max((field as NumberField).max_value || Infinity);
                                break;
                            case 'checkbox':
                                base = (field as CheckboxField).required ? z.literal(true) : z.boolean();
                                break;
                            case 'number_pair':
                                base = z.array(((field as NumberField).is_float ? z.number() : z.number().int())).length(2);
                                break;
                            case 'select':
                                base = z.any();
                                break;
                            case 'multiselect':
                                base = z.array(z.any()).min((field as MultiSelectField).min_selected).max((field as MultiSelectField).max_selected || Infinity);
                                break;
                            case 'percentage':
                                base = z.number().max(100).min(0);
                                break
                            case 'model_select':
                                base = z.string();
                                break
                            default:
                                throw new Error(`Unknown field type: ${field.type}`);
                        }

                        const nestedPaths = layout.nestedPaths
                            ? [...layout.nestedPaths, ...field.nested_paths]
                            : field.nested_paths;

                        if (nestedPaths.length) {
                            const nestedSchema = buildSchema([{
                                sections: [{
                                    id: '',
                                    title: '',
                                    subsections: [{
                                        id: '',
                                        title: '',
                                        model_parameters: false,
                                        lines: [{ fields: [{ ...field, nested_paths: nestedPaths.slice(1) }] }]
                                    }]
                                }]
                            }]);

                            schema[nestedPaths[0]] = schema[nestedPaths[0]]
                                ? (schema[nestedPaths[0]] as z.ZodObject<any>).merge(nestedSchema)
                                : nestedSchema;
                        } else {
                            schema[field.name] = base;
                        }
                    }
                }
            }
        }
    }

    return z.object(schema);
}

function getLayoutValues(layouts: SchemaBuilderLayout[]) {
    const values = {} as Record<string, any>;

    for (const layout of layouts) {
        for (const section of layout.sections) {
            for (const subsection of section.subsections) {
                for (const line of subsection.lines) {
                    for (const field of line.fields) {
                        const nestedPaths = layout.nestedPaths
                            ? [...layout.nestedPaths, ...field.nested_paths]
                            : field.nested_paths;

                        if (nestedPaths.length) {

                            const nestedValues = getLayoutValues([{
                                sections: [{
                                    id: '',
                                    title: '',
                                    subsections: [{
                                        id: '',
                                        title: '',
                                        model_parameters: false,
                                        lines: [{ fields: [{ ...field, nested_paths: nestedPaths.slice(1) }] }]
                                    }]
                                }]
                            }]);

                            values[nestedPaths[0]] = values[nestedPaths[0]]
                                ? { ...values[nestedPaths[0]], ...nestedValues }
                                : nestedValues;
                        } else {
                            values[field.name] = field.value;
                        }
                    }
                }
            }
        }
    }

    return values;
}

function getModelNameFieldsPathsAndSections(layouts: SchemaBuilderLayout[]) {
    const values: Record<string, SectionType> = {};

    for (const layout of layouts) {
        for (const section of layout.sections) {
            for (const subsection of section.subsections) {
                for (const line of subsection.lines) {
                    for (const field of line.fields) {
                        if (field.type !== 'model_select') continue;

                        const nestedPaths = layout.nestedPaths
                            ? [...layout.nestedPaths, ...field.nested_paths, field.name]
                            : [...field.nested_paths, field.name];

                        values[nestedPaths.join('.')] = section;
                    }
                }
            }
        }
    }

    return values;
}

export type ConfigFormSchema = {
    simulation_name: string,
    asynchronous: boolean,
    dim_x: number[],
    dim_y: number[],
    nack_messages_enabled: boolean,
    save_trace: boolean,
    connectivity_enabled: boolean,
    interference_enabled: boolean,
    message_transmission_model: string,
    message_transmission_model_parameters: Record<string, any>,
    project_config: Record<string, any>,
    [key: string]: any,
}

export type SuperSection = {
    id: string,
    title: string,
    prefix: string,
    styleClasses: {
        superSection: string[],
        superSectionTitle: string[],
        section: string[],
        sectionTitle: string[],
        subSection: string[],
        line: string[]
    },
    layout: Layout | undefined | null,
    nestedPaths?: string[]
}

type ConfigFormProps = {
    project_name: string
}
export default function ConfigForm({
    project_name
}: ConfigFormProps) {
    const [simulationConfigLayout, setSimulationConfigLayout] = useState<Layout>();
    const [projectConfigLayout, setProjectConfigLayout] = useState<Layout | null>();
    const [configFormSchema, setConfigFormSchema] = useState<z.ZodObject<ConfigFormSchema>>();
    const [modelNameFields, setModelNameFields] = useState<string[]>([]);
    const [modelNameFieldsPathsAndSections, setModelNameFieldsPathsAndSections] = useState<Record<string, SectionType>>({});
    const { showModal } = useErrorModal();

    const {
        register,
        control,
        handleSubmit,
        formState: { errors: formErrors },
        reset,
        watch,
    } = useForm<ConfigFormSchema>({
        resolver: configFormSchema ? zodResolver(configFormSchema as unknown as Parameters<typeof zodResolver<ConfigFormSchema, any, ConfigFormSchema>>[0]) : undefined,
    });

    const {
        data: configFormLayout,
        error: configFormLayoutError,
        isLoading: isLoadingConfigFormLayout,
    } = useSWR(`config_form_layout_${project_name}`, () => fetchConfigFormLayout(project_name));
    const { data: config, error: configError, isLoading: isLoadingConfig } = useSWR(`config_${project_name}`, () => fetchConfigForm(project_name));

    const superSections: SuperSection[] = useMemo(() => [
        {
            id: 'global-simulation-config',
            title: 'Global Simulation Config',
            prefix: 'global_simulation',
            styleClasses: {
                superSection: [],
                superSectionTitle: [],
                section: [],
                sectionTitle: [],
                subSection: [],
                line: []
            },
            layout: simulationConfigLayout,
        },
        ...(projectConfigLayout ? [{
            id: 'project-config',
            title: 'Project Config',
            prefix: 'project',
            styleClasses: {
                superSection: [],
                superSectionTitle: [],
                section: [],
                sectionTitle: [],
                subSection: [],
                line: []
            },
            layout: projectConfigLayout,
            nestedPaths: ['project_config']
        }] : []),
    ], [simulationConfigLayout, projectConfigLayout]);

    const updateModelSections = useCallback(async (inputName: string | undefined) => {
        if (!inputName || !modelNameFields.includes(inputName) || !config) return;

        const modelName: string = watch(inputName);
        const section = modelNameFieldsPathsAndSections[inputName];
        const modelSubsectionLayout = await fetchModelSubsectionLayout(modelName, section.model_type!);

        if (inputName.startsWith('project_config')) {
            setProjectConfigLayout((projectConfigLayout) => ({
                sections: [
                    ...(projectConfigLayout?.sections.map((section_) => {
                        return {
                            ...section_,
                            subsections: section_.subsections.map((subsection) => getCorrectSubsection(subsection, section_))
                        }
                    }) ?? []),
                ]
            }));
        } else {
            setSimulationConfigLayout((simulationConfigLayout) => (simulationConfigLayout ? {
                sections: [
                    ...(simulationConfigLayout.sections.map((section_) => {
                        return {
                            ...section_,
                            subsections: section_.subsections.map((subsection) => getCorrectSubsection(subsection, section_))
                        }
                    }) ?? [])
                ]
            } : undefined));
        }

        function getCorrectSubsection(subsection: Subsection, section_: SectionType): Subsection {

            if (!subsection.model_parameters) return subsection;

            const isTheTarget = inputName!.split('.').slice(0, -1).join('.').endsWith(section.subsections[0].lines[0].fields[0].nested_paths.join('.')) && section_.model_type === section.model_type && subsection.model_parameters;

            if (!isTheTarget) return subsection;
            return modelSubsectionLayout;
        }
    }, [config, watch, modelNameFieldsPathsAndSections, modelNameFields]);



    useEffect(() => {
        if (config && configFormLayout) {
            reset({ ...watch(), ...config, project_config: { ...watch().project_config, ...config.project_config } });
            modelNameFields.forEach((inputName) => {
                updateModelSections(inputName);
            });
        }
    }, [config]);

    // set defaults values when config form layout is loaded
    useEffect(() => {
        if (configFormLayout) {
            const layouts = [
                configFormLayout.simulation_config_layout,
                ...(configFormLayout.project_config_layout
                    ? [{ ...configFormLayout.project_config_layout, nestedPaths: ['project_config'] }]
                    : [])
            ]

            reset(getLayoutValues(layouts));

            setSimulationConfigLayout(configFormLayout.simulation_config_layout);
            setProjectConfigLayout(configFormLayout.project_config_layout);

            const modelNameFieldsPathsAndSections = getModelNameFieldsPathsAndSections(layouts);
            setModelNameFields(Object.keys(modelNameFieldsPathsAndSections));
            setModelNameFieldsPathsAndSections(modelNameFieldsPathsAndSections);
        }
    }, [configFormLayout]);

    // set config form schema everyTime superSections change (superSections defines the structure of the form)
    useEffect(() => {
        const layouts = superSections
            .map((superSection) => superSection.layout ? ({ ...superSection.layout, nestedPaths: superSection.nestedPaths! }) : undefined)
            .filter((x) => x) as SchemaBuilderLayout[];

        setConfigFormSchema(buildSchema(layouts) as unknown as z.ZodObject<ConfigFormSchema>);

        reset({ ...config, ...watch(), project_config: { ...config?.project_config, ...watch().project_config } });
    }, [superSections]);

    useEffect(() => {
        if (configFormLayoutError) {
            console.error(configFormLayoutError);
            toastError('Error loading config form layout');
        }
    }, [configFormLayoutError]);

    useEffect(() => {
        if (formErrors && Object.keys(formErrors).length > 0) {
            console.error(formErrors);
            toastError('Error validating config form');
            showModal(<ReactJson
                src={formErrors}
                name={'formErrors'}
                collapsed={false}
                enableClipboard={true}
                displayDataTypes={false}
                quotesOnKeys={false}
                theme="rjv-default"
            />, 'Error validating config form');
        }
    }, [formErrors]);

    useEffect(() => {
        if (configError) {
            console.error(configError);
            toastError('Error loading config data');
        }
    }, [configError]);

    const handleConfigSubmit = (data: ConfigFormSchema) => {
        console.log('submited form data:', data);
        updateConfig(project_name, data)
            .then(() => {
                toast.success(`Config of project ${project_name} updated`);
            })
            .catch((error) => {
                console.error(error);
                toastError('Error updating config');
                return;
            });
    }

    if (configFormLayoutError) return;

    if (isLoadingConfigFormLayout) return (
        <div className="w-full h-full flex items-center justify-center text-3xl">Loading form layout...</div>
    )



    return (
        <form
            className={clsx("flex", "flex-col", "gap-8")}
            onSubmit={handleSubmit(handleConfigSubmit)}
            id="config-form"
        >
            {superSections.map((superSection) => {
                return (
                    <div
                        key={superSection.id}
                        id={superSection.id}
                        className={clsx(superSection.id, 'w-full', 'p-4', 'rounded-md', 'shadow-lg', ...superSection.styleClasses.superSection)}
                    >
                        <h2
                            className={clsx('text-3xl', 'mb-2', ...superSection.styleClasses.superSectionTitle)}
                        >{superSection.title}</h2>

                        {superSection.layout?.sections.map((section, sectionIndex) => {
                            return (
                                <Section
                                    control={control}
                                    isLoadingConfig={isLoadingConfig}
                                    register={register}
                                    section={section}
                                    nestedPaths={superSection.nestedPaths}
                                    superSection={superSection}
                                    key={section.id + sectionIndex}
                                    onModelNameChange={updateModelSections}
                                />
                            )
                        })}
                    </div>
                )
            })}


            <div className="flex justify-end">
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Submit
                </button>
            </div>
        </form>
    )
}