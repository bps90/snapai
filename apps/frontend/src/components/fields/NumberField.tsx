import { FormControl, FormControlProps, TextField, TextFieldProps } from "@mui/material";
import { FormFieldProps } from "./FormField";
import { Field } from '@/lib/fetchers';
import { ConfigFormSchema } from "../ConfigForm";


export type NumberField = Field & {
    type: 'number',
    is_float: boolean,
    value: number
}

type NumberFieldProps = FormFieldProps & {
    field: NumberField,
    formControlAttr?: FormControlProps,
    inputAttr?: TextFieldProps,
}

export default function NumberField({
    field,
    fieldIndex,
    register,
    containerAttr,
    formControlAttr,
    inputAttr
}: NumberFieldProps) {
    return (<div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
    >
        <FormControl fullWidth {...formControlAttr}>
            <TextField
                variant='outlined'
                label={field.label}
                type={field.type}
                slotProps={{ htmlInput: { step: field.is_float ? 'any' : '1' } }}
                id={field.id}
                required={field.required}
                defaultValue={field.value}
                {...register(field.name as keyof ConfigFormSchema)}
                {...inputAttr}
            />
        </FormControl>
    </div>);
}