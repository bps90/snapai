/* eslint-disable @typescript-eslint/no-explicit-any */
import { toastError } from "@/hooks/toastError";
import { fetchConfigForm, fetchConfigFormLayout, Layout } from "@/lib/fetchers";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import useSWR from "swr";
import { z } from 'zod'
import clsx from 'clsx'
import Section from "./formDivisions/Section";



function buildSchema(layouts: Layout[]) {
    const schema: Record<string, z.ZodType> = {};

    for (const layout of layouts) {
        for (const section of layout.sections) {
            for (const subsection of section.subsections) {
                for (const line of subsection.lines) {
                    for (const field of line.fields) {
                        let base: z.ZodType;

                        switch (field.type) {
                            case 'text':
                                base = z.string();
                                break;
                            case 'number':
                                base = z.number();
                                break;
                            case 'checkbox':
                                base = z.boolean();
                                break;
                            case 'number_pair':
                                base = z.array(z.number());
                                break;
                            case 'select':
                                base = z.string();
                                break;
                            case 'multiselect':
                                base = z.array(z.string());
                                break;
                            case 'percentage':
                                base = z.number().max(100).min(0);
                            default:
                                throw new Error(`Unknown field type: ${field.type}`);
                        }


                        if (field.nested_paths.length) {
                            const nestedSchema = buildSchema([{
                                sections: [
                                    {
                                        id: '',
                                        title: '',
                                        subsections: [
                                            {
                                                id: '',
                                                title: '',
                                                lines: [
                                                    {
                                                        fields: [
                                                            {
                                                                ...field,
                                                                nested_paths: field.nested_paths.slice(1),
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }]);

                            schema[field.nested_paths[0]] = schema[field.nested_paths[0]]
                                ? (schema[field.nested_paths[0]] as z.ZodObject<any>).merge(nestedSchema)
                                : nestedSchema;
                        } else {
                            schema[field.name] = base;
                        }
                    }
                }
            }
        }
    }

    console.log(schema);

    return z.object(schema);
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
    const { register, control, handleSubmit, formState: { errors: formErrors } } = useForm<ConfigFormSchema>({
        resolver: configFormSchema ? zodResolver(configFormSchema as unknown as Parameters<typeof zodResolver<ConfigFormSchema, any, ConfigFormSchema>>[0]) : undefined
    });

    const { data: configFormLayout, error: configFormLayoutError, isLoading: isLoadingConfigFormLayout } = useSWR(`config_form_layout_${project_name}`, () => fetchConfigFormLayout(project_name));
    const { data: config, error: configError, isLoading: isLoadingConfig } = useSWR(`config_${project_name}`, () => fetchConfigForm(project_name));

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
            setConfigFormSchema(buildSchema([
                configFormLayout.simulation_config_layout,
                ...(configFormLayout.project_config_layout ? [configFormLayout.project_config_layout] : [])
            ]) as unknown as z.ZodType<ConfigFormSchema>);
        }
    }, [configFormLayout])


    const handleConfigSubmit = (data: ConfigFormSchema) => {
        console.log(data);
    }

    if (configFormLayoutError) return;

    if (isLoadingConfigFormLayout) return (
        <div className="w-full h-full flex items-center justify-center text-3xl">Loading form layout...</div>
    )

    const superSectionStyleClasses = [
        'w-full',
        'p-4',
        'rounded-md',
        'shadow-lg',
    ];

    const superSectionTitleStyleClasses = [
        'text-3xl',
        'mb-2'
    ];

    const sectionStyleClasses = [
        'border',
        'rounded-md',
        'border-gray-200',
        'p-2',
        'mb-2',
        'flex',
        'flex-col',
        'gap-6'
    ];

    const sectionTitleStyleClasses = [
        'text-2xl',
        'mb-2'
    ];


    const subSectionStyleClasses = [
        'flex',
        'flex-col',
        'gap-3'
    ];

    const lineStyleClasses = [
        'grid',
        'grid-cols-12',
        'gap-3'
    ]

    const superSections: SuperSection[] = [
        {
            id: 'global-simulation-config',
            title: 'Global Simulation Config',
            prefix: 'global_simulation',
            styleClasses: {
                superSection: ['mb-8', ...superSectionStyleClasses],
                superSectionTitle: superSectionTitleStyleClasses,
                section: sectionStyleClasses,
                sectionTitle: sectionTitleStyleClasses,
                subSection: subSectionStyleClasses,
                line: lineStyleClasses
            },
            layout: simulationConfigLayout,
        },
        {
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
            layout: projectConfigLayout
        }
    ]

    return (
        <form
            className={clsx()}
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