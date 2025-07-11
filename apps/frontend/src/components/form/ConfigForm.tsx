/* eslint-disable @typescript-eslint/no-explicit-any */
import { toastError } from "@/hooks/toastError";
import { fetchConfigForm, fetchConfigFormLayout, Layout } from "@/lib/fetchers";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import useSWR from "swr";
import { z } from 'zod'
import clsx from 'clsx'
import Section from "./formDivisions/Section";
import { TextField } from "./fields/TextField";
import { NumberField } from "./fields/NumberField";
import { CheckboxField } from "./fields/CheckboxField";
import { MultiSelectField } from "./fields/MultiSelectField";


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
    const [configFormSchema, setConfigFormSchema] = useState<z.ZodType<ConfigFormSchema>>();
    const {
        register,
        control,
        handleSubmit,
        formState: { errors: formErrors },
        reset,
        watch
    } = useForm<ConfigFormSchema>({
        resolver: configFormSchema ? zodResolver(configFormSchema as unknown as Parameters<typeof zodResolver<ConfigFormSchema, any, ConfigFormSchema>>[0]) : undefined,
    });

    const {
        data: configFormLayout,
        error: configFormLayoutError,
        isLoading: isLoadingConfigFormLayout,
    } = useSWR(`config_form_layout_${project_name}`, () => fetchConfigFormLayout(project_name));
    const { data: config, error: configError, isLoading: isLoadingConfig } = useSWR(`config_${project_name}`, () => fetchConfigForm(project_name));

    const superSectionStyleClasses = useMemo(() => [
        'w-full',
        'p-4',
        'rounded-md',
        'shadow-lg',
    ], []);

    const superSectionTitleStyleClasses = useMemo(() => [
        'text-3xl',
        'mb-2'
    ], []);

    const sectionStyleClasses = useMemo(() => [
        'border',
        'rounded-md',
        'border-gray-200',
        'p-2',
        'mb-2',
        'flex',
        'flex-col',
        'gap-6'
    ], []);

    const sectionTitleStyleClasses = useMemo(() => [
        'text-2xl',
        'mb-2'
    ], []);


    const subSectionStyleClasses = useMemo(() => [
        'flex',
        'flex-col',
        'gap-3'
    ], []);

    const lineStyleClasses = useMemo(() => [
        'grid',
        'grid-cols-12',
        'gap-3'
    ], []);

    const superSections: SuperSection[] = useMemo(() => [
        {
            id: 'global-simulation-config',
            title: 'Global Simulation Config',
            prefix: 'global_simulation',
            styleClasses: {
                superSection: superSectionStyleClasses,
                superSectionTitle: superSectionTitleStyleClasses,
                section: sectionStyleClasses,
                sectionTitle: sectionTitleStyleClasses,
                subSection: subSectionStyleClasses,
                line: lineStyleClasses
            },
            layout: simulationConfigLayout,
        },
        ...(projectConfigLayout ? [{
            id: 'project-config',
            title: 'Project Config',
            prefix: 'project',
            styleClasses: {
                superSection: superSectionStyleClasses,
                superSectionTitle: superSectionTitleStyleClasses,
                section: sectionStyleClasses,
                sectionTitle: sectionTitleStyleClasses,
                subSection: subSectionStyleClasses,
                line: lineStyleClasses
            },
            layout: projectConfigLayout,
            nestedPaths: ['project_config']
        }] : []),
    ], [
        simulationConfigLayout,
        projectConfigLayout,
        superSectionStyleClasses,
        superSectionTitleStyleClasses,
        sectionStyleClasses,
        sectionTitleStyleClasses,
        subSectionStyleClasses,
        lineStyleClasses
    ]);

    useEffect(() => {
        if (config) {
            reset({
                ...watch(),
                ...config
            });
        }
    }, [config, reset, watch]);

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
        }
    }, [formErrors]);

    useEffect(() => {
        if (configError) {
            console.error(configError);
            toastError('Error loading config data');
        }
    }, [configError]);

    useEffect(() => {
        if (configFormLayout) {
            setSimulationConfigLayout(configFormLayout.simulation_config_layout);
            setProjectConfigLayout(configFormLayout.project_config_layout);
        }
    }, [configFormLayout]);

    useEffect(() => {
        if (configFormLayout) {
            const layouts = superSections
                .map((superSection) => superSection.layout ? ({ ...superSection.layout, nestedPaths: superSection.nestedPaths! }) : undefined)
                .filter((x) => x) as SchemaBuilderLayout[];

            setConfigFormSchema(buildSchema(layouts) as unknown as z.ZodType<ConfigFormSchema>);
            reset(getLayoutValues(layouts));
        }
    }, [configFormLayout, superSections, reset]);


    const handleConfigSubmit = (data: ConfigFormSchema) => {
        console.log('submited form data:', data);
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
                        className={clsx(superSection.id, ...superSection.styleClasses.superSection)}
                    >
                        <h2
                            className={clsx(...superSection.styleClasses.superSectionTitle)}
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