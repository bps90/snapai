import { Line as LineType, Section, Subsection } from "@/lib/fetchers"
import { ConfigFormSchema, SuperSection } from "../ConfigForm";
import clsx from "clsx";
import FormField from "@/components/form/fields/FormField";
import { Control, UseFormRegister } from "react-hook-form";

export type LineProps = {
    subsection: Subsection;
    line: LineType;
    lineIndex: number;
    section: Section;
    superSection: SuperSection;
    register: UseFormRegister<ConfigFormSchema>;
    control: Control<ConfigFormSchema>;
    isLoadingConfig: boolean;
    nestedPaths?: string[];
    [key: string]: unknown;
}

export default function Line({
    subsection,
    lineIndex,
    superSection,
    section,
    line,
    control,
    register,
    isLoadingConfig,
    nestedPaths,
    ...props
}: LineProps) {
    return (
        <div
            id={`${superSection.prefix}_line_${section.id}_${subsection.id}_index_${lineIndex}`}
            className={clsx(
                `${superSection.prefix}_line_${subsection.id}_index_${lineIndex}`,
                'grid', 'grid-cols-12', 'gap-3', 'items-end',
                ...superSection.styleClasses.line
            )}
        >
            {line.fields.map((field, fieldIndex) => {
                return <FormField
                    nestedPaths={nestedPaths}
                    control={control}
                    field={field}
                    fieldIndex={fieldIndex}
                    register={register}
                    key={field.id + fieldIndex}
                    disabled={isLoadingConfig}
                    {...props}
                ></FormField>
            })}
        </div>
    )
}