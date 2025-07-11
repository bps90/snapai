import { Field } from "@/lib/fetchers"
import { FormFieldProps } from "./FormField"
import { FormControl, FormControlProps, InputLabel, MenuItem, Select, SelectProps } from "@mui/material"
import { Controller } from "react-hook-form"

export type SelectField = Field & {
    type: 'select',
    value: unknown,
    options: ({ value: unknown, label: string })[]
}

export type SelectFieldProps = FormFieldProps & {
    field: SelectField,
    formControlAttr?: FormControlProps,
    selectAttr?: SelectProps
}

export default function SelectField({
    nestedPaths,
    field,
    control,
    selectAttr,
    formControlAttr,
    fieldIndex,
    containerAttr,
}: SelectFieldProps) {
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
                    defaultValue={field.value ?? ''}
                    rules={{ required: field.required }}
                    render={({ field: controllerField }) => (
                        <Select
                            labelId={name + '__label'}
                            variant="outlined"
                            label={field.label}
                            id={field.id}
                            value={controllerField.value ?? ''}
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