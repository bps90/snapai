import { Section, Subsection } from "@/lib/fetchers"
import { Control, UseFormRegister } from "react-hook-form"
import { ConfigFormSchema, SuperSection } from "../ConfigForm"
import clsx from "clsx"
import Line from "./Line"

export type SubSectionProps = {
    superSection: SuperSection
    section: Section
    subsection: Subsection
    subsectionIndex: number
    control: Control<ConfigFormSchema>
    register: UseFormRegister<ConfigFormSchema>
    isLoadingConfig: boolean;
    nestedPaths?: string[];
    [key: string]: unknown
}

export default function SubSection({
    superSection,
    control,
    isLoadingConfig,
    register,
    section,
    subsection,
    subsectionIndex,
    nestedPaths,
    ...props
}: SubSectionProps) {
    return (
        <fieldset
            id={`${superSection.prefix}_subsection_${section.id}_${subsection.id}`}
            className={clsx(
                `${superSection.prefix}_subsection_${subsection.id}`,
                'flex', 'flex-col', 'gap-3',
                ...superSection.styleClasses.subSection
            )}
        >
            {subsection.title && <legend>{subsection.title}</legend>}

            {subsection.lines.map((line, lineIndex) => {
                return (
                    <Line
                        control={control}
                        isLoadingConfig={isLoadingConfig}
                        line={line}
                        lineIndex={lineIndex}
                        register={register}
                        section={section}
                        subsection={subsection}
                        superSection={superSection}
                        nestedPaths={nestedPaths}
                        key={`subsection_${subsection.id + subsectionIndex}_line${lineIndex}`}
                        {...props}
                    />

                )
            })}
        </fieldset>
    )
}