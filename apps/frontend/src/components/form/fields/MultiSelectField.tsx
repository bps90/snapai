import { Field } from "@/lib/fetchers"
import { FormFieldProps } from "./FormField"
import { FormControl, FormControlProps, InputLabel, MenuItem, Select, SelectProps } from "@mui/material"
import { Controller } from "react-hook-form"

export type MultiSelectField = Field & {
    type: 'multiselect',
    value: unknown[],
    options: ({ value: unknown, label: string })[],
    min_selected: number,
    max_selected: number | null
}

export type MultiSelectFieldProps = FormFieldProps & {
    field: MultiSelectField,
    formControlAttr?: FormControlProps,
    selectAttr?: SelectProps
}

export default function MultiSelectField({
    nestedPaths,
    field,
    control,
    selectAttr,
    formControlAttr,
    fieldIndex,
    containerAttr,
}: MultiSelectFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];
    const name = nameAsArray.join('.');

    return (
        <div
            key={field.id + fieldIndex}
            style={{ gridColumn: `span ${field.occuped_columns}` }}
            {...containerAttr}
        >
            <FormControl fullWidth {...formControlAttr}>
                <InputLabel id={name + '__label'}>{field.label}</InputLabel>
                <Controller
                    name={name}
                    control={control}
                    defaultValue={field.value ?? []}
                    rules={{ required: field.required }}
                    render={({ field: controllerField }) => (
                        <Select
                            labelId={name + '__label'}
                            multiple
                            variant="outlined"
                            label={field.label}
                            id={field.id}
                            value={controllerField.value || []}
                            onChange={controllerField.onChange}
                            {...selectAttr}
                        >
                            {field.options.map((option, optionIndex) => (
                                <MenuItem
                                    key={`${option.value}_${optionIndex}`}
                                    value={option.value as string | number}
                                >
                                    {option.label}
                                </MenuItem>
                            ))}
                        </Select>
                    )}
                />
            </FormControl>
        </div>
    );
}