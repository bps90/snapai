import { Section as SectionType } from "@/lib/fetchers"
import { ConfigFormSchema, SuperSection } from "../ConfigForm"
import clsx from "clsx";
import SubSection from "./SubSection";
import { Control, UseFormRegister } from "react-hook-form";

export type SectionProps = {
    section: SectionType;
    superSection: SuperSection;
    control: Control<ConfigFormSchema>;
    isLoadingConfig: boolean;
    register: UseFormRegister<ConfigFormSchema>;
    nestedPaths?: string[];
    [key: string]: unknown
}


export default function Section({
    superSection,
    section,
    control,
    isLoadingConfig,
    register,
    nestedPaths,
    ...props
}: SectionProps) {
    return (
        <div
            id={`${superSection.prefix}_section_${section.id}`}
            className={clsx(`${superSection.prefix}_section_${section.id}`, 'border', 'rounded-md', 'border-gray-200', 'p-2', 'mb-2', 'flex', 'flex-col', 'gap-6', ...superSection.styleClasses.section)}
        >
            <h3 className={clsx('text-2xl', 'mb-2', ...superSection.styleClasses.sectionTitle)}>{section.title}</h3>

            {section.subsections.map((subsection, subsectionIndex) => {
                return (
                    <SubSection
                        control={control}
                        isLoadingConfig={isLoadingConfig}
                        register={register}
                        section={section}
                        subsection={subsection}
                        subsectionIndex={subsectionIndex}
                        superSection={superSection}
                        nestedPaths={nestedPaths}
                        key={subsection.id + subsectionIndex}
                        {...props}
                    />

                )
            })}
        </div>
    )
}