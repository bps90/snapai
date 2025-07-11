import { FormControl, FormControlProps, InputAdornment, TextField, TextFieldProps } from "@mui/material";
import { FormFieldProps } from "./FormField";
import { NumberField } from "./NumberField";


export type PercentageField = Omit<NumberField, 'type'> & {
    type: 'percentage',
}

type PercentageFieldProps = FormFieldProps & {
    field: PercentageField,
    formControlAttr?: FormControlProps,
    inputAttr?: TextFieldProps,
}

export default function PercentageField({
    field,
    fieldIndex,
    register,
    containerAttr,
    formControlAttr,
    inputAttr,
    nestedPaths
}: PercentageFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];

    return (<div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
    >
        <FormControl fullWidth {...formControlAttr}>
            <TextField
                variant='outlined'
                label={field.label}
                type={'number'}
                slotProps={{
                    htmlInput: { step: field.is_float ? 'any' : '1', min: field.min_value, max: field.max_value },
                    input: { endAdornment: <InputAdornment position="end">%</InputAdornment> }
                }}
                id={field.id}
                required={field.required}
                {...register(nameAsArray.join('.'), { valueAsNumber: true })}
                {...inputAttr}
            />
        </FormControl>
    </div>);
}