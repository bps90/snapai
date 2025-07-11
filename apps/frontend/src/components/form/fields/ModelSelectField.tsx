import { FormFieldProps } from "./FormField"
import { FormControl, FormControlProps, InputLabel, MenuItem, Select, SelectProps } from "@mui/material"
import { SelectField } from "./SelectField"
import { Controller } from "react-hook-form"

export type ModelSelectField = Omit<SelectField, 'type' | 'value' | 'options'> & {
    type: 'model_select',
    model_type: 'connectivity' | 'mobility' | 'interference' | 'reliability' | 'distribution' | 'message_transmission'
    value: string,
    options: ({ value: string, label: string })[]
}

export type ModelSelectFieldProps = FormFieldProps & {
    field: ModelSelectField,
    formControlAttr?: FormControlProps,
    selectAttr?: SelectProps
}

export default function ModelSelectField({
    nestedPaths,
    field,
    control,
    selectAttr,
    formControlAttr,
    fieldIndex,
    containerAttr,
}: ModelSelectFieldProps) {
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
                            {...controllerField}
                            {...selectAttr}
                        >
                            {field.options.map((option, optionIndex) => (
                                <MenuItem
                                    key={`${option.value}_${optionIndex}`}
                                    value={option.value}
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