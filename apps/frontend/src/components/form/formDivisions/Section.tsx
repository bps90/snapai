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
}


export default function Section({
    superSection,
    section,
    control,
    isLoadingConfig,
    register,
    nestedPaths
}: SectionProps) {
    return (
        <div
            id={`${superSection.prefix}_section_${section.id}`}
            className={clsx(`${superSection.prefix}_section_${section.id}`, ...superSection.styleClasses.section)}
        >
            <h3 className={clsx(...superSection.styleClasses.sectionTitle)}>{section.title}</h3>

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
                    />

                )
            })}
        </div>
    )
}