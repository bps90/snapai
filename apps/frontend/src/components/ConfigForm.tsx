import { toastError } from "@/hooks/toastError";
import { fetchConfigFormLayout, Layout } from "@/lib/fetchers";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import useSWR from "swr";
import { z } from 'zod'
import FormField from "./fields/FormField";
import clsx from 'clsx'

const configFormSchema = z.object({
    simulation_name: z.string(),
    asynchronous: z.boolean(),
    dim_x: z.array(z.number()),
    dim_y: z.array(z.number()),
    nack_messages_enabled: z.boolean(),
    save_trace: z.boolean()
})

export type ConfigFormSchema = z.infer<typeof configFormSchema>

type ConfigFormProps = {
    project_name: string
}
export default function ConfigForm({
    project_name
}: ConfigFormProps) {
    const [simulationConfigLayout, setSimulationConfigLayout] = useState<Layout>();
    const [projectConfigLayout, setProjectConfigLayout] = useState<Layout | null>();
    const { register, control, handleSubmit, formState: { errors } } = useForm<ConfigFormSchema>({
        resolver: zodResolver(configFormSchema)
    });
    const { data: configFormLayout, error: configFormLayoutError, isLoading: isLoadingConfigFormLayout } = useSWR(`config_form_layout_${project_name}`, () => fetchConfigFormLayout(project_name));

    useEffect(() => {
        if (configFormLayoutError) {
            console.error(configFormLayoutError);
            toastError('Error loading config form layout');
        }
    }, [configFormLayoutError]);

    useEffect(() => {
        if (errors) {
            console.error(errors);
            toastError('Error validating config form');
        }
    }, [errors]);

    useEffect(() => {
        if (configFormLayout) {
            setSimulationConfigLayout(configFormLayout.simulation_config_layout);
            setProjectConfigLayout(configFormLayout.project_config_layout)
        }
    }, [configFormLayout])

    const handleConfigSubmit = (data: ConfigFormSchema) => {
        console.log(data);
    }

    if (configFormLayoutError) return;

    if (isLoadingConfigFormLayout) return (
        <div className="w-full h-full flex items-center justify-center text-3xl">Loading form layout...</div>
    )

    return (
        <form
            className={clsx()}
            onSubmit={handleSubmit(handleConfigSubmit)}
            id="config-form"
        >
            <div id="global-simulation-config" className={clsx(
                "simulation-config",
                "w-full",
                "p-4",
                "mb-8",
                "rounded-md",
                "shadow-lg",
            )}>
                <h2
                    className="text-2xl mb-2"
                >Global Simulation Config</h2>

                {simulationConfigLayout?.sections.map((section, sectionIndex) => {
                    return (
                        <div
                            key={section.id + sectionIndex}
                            id={`simulation_section_${section.id}`}
                            className={clsx(
                                `simulation_section_${section.id}`,
                                'border',
                                'rounded-md',
                                'border-gray-200',
                                'p-2',
                                'mb-2'
                            )}
                        >
                            <h3
                                className={clsx(
                                    "text-2xl",
                                    "mb-4",
                                )}
                            >{section.title}</h3>
                            {section.subsections.map((subsection, subsectionIndex) => {
                                return (
                                    <fieldset
                                        key={subsection.id + subsectionIndex}
                                        id={`simulation_subsection_${section.id}_${subsection.id}`}
                                        className={clsx(
                                            `simulation_subsection_${subsection.id}`,
                                            'flex',
                                            'flex-col',
                                            'gap-3'
                                        )}
                                    >
                                        {subsection.title && <legend>{subsection.title}</legend>}

                                        {subsection.lines.map((line, lineIndex) => {
                                            return (
                                                <div
                                                    key={`subsection_${subsection.id + subsectionIndex}_line${lineIndex}`}
                                                    id={`simulation_line_${section.id}_${subsection.id}_index_${lineIndex}`}
                                                    className={clsx(
                                                        `simulation_line_${subsection.id}_index_${lineIndex}`,
                                                        'grid',
                                                        'grid-cols-12',
                                                        'gap-3'
                                                    )}
                                                >
                                                    {line.fields.map((field, fieldIndex) => {
                                                        return <FormField
                                                            control={control}
                                                            field={field}
                                                            fieldIndex={fieldIndex}
                                                            register={register}
                                                            key={field.id + fieldIndex}
                                                        ></FormField>
                                                    })}
                                                </div>
                                            )
                                        })}
                                    </fieldset>
                                )
                            })}
                        </div>
                    )
                })}
            </div>

            {projectConfigLayout && <div id="project-config" className={clsx(
                "project-config",
                "w-full",
                "p-4",
                "rounded-md",
                "shadow-lg",
            )}>
                <h2
                    className="text-2xl mb-2"
                >Project Config</h2>


                {projectConfigLayout.sections.map((section, sectionIndex) => {
                    return (
                        <div
                            key={section.id + sectionIndex}
                            id={`project_section_${section.id}`}
                            className={clsx(
                                `project_section_${section.id}`,
                                'border',
                                'rounded-md',
                                'border-gray-200',
                                'p-2',
                                'mb-2'
                            )}
                        >
                            <h3
                                className={clsx(
                                    "text-2xl",
                                    "mb-4",
                                )}
                            >{section.title}</h3>
                            {section.subsections.map((subsection, subsectionIndex) => {
                                return (
                                    <fieldset
                                        key={subsection.id + subsectionIndex}
                                        id={`project_subsection_${section.id}_${subsection.id}`}
                                        className={`project_subsection_${subsection.id}`}
                                    >
                                        {subsection.title && <legend>{subsection.title}</legend>}

                                        {subsection.lines.map((line, lineIndex) => {
                                            return (
                                                <div
                                                    key={`subsection_${subsection.id + subsectionIndex}_line${lineIndex}`}
                                                    id={`project_line_${section.id}_${subsection.id}_index_${lineIndex}`}
                                                    className={clsx(
                                                        `project_line_${subsection.id}_index_${lineIndex}`,
                                                        'grid',
                                                        'grid-cols-12',
                                                        'gap-3'
                                                    )}
                                                >
                                                    {line.fields.map((field, fieldIndex) => {
                                                        return <FormField
                                                            control={control}
                                                            field={field}
                                                            fieldIndex={fieldIndex}
                                                            register={register}
                                                            key={field.id + fieldIndex}
                                                        ></FormField>
                                                    })}
                                                </div>
                                            )
                                        })}
                                    </fieldset>
                                )
                            })}
                        </div>
                    )
                })}
            </div>}

            <div className="flex justify-end">
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Save
                </button>
            </div>
        </form>
    )
}