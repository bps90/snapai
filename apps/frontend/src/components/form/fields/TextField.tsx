import { Field } from '@/lib/fetchers';
import { FormControl, FormControlProps, TextField as MaterialTextField, TextFieldProps as MaterialTextFieldProps, TextField } from '@mui/material';
import { FormFieldProps } from './FormField';

export type TextField = Field & {
    type: 'text'
    value: string
}

export type TextFieldProps = FormFieldProps & {
    inputAttr?: MaterialTextFieldProps,
    formControlAttr?: FormControlProps,
    field: TextField,
}

function TextField({
    field, fieldIndex,
    inputAttr,
    containerAttr,
    formControlAttr,
    nestedPaths,
    register
}: TextFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];

    return <div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
    >
        <FormControl fullWidth {...formControlAttr}>
            <MaterialTextField
                variant='outlined'
                label={field.label}
                type={field.type}
                id={field.id}
                required={field.required}
                {...register(nameAsArray.join('.'))}
                {...inputAttr}
            />
        </FormControl>
    </div>;
}

export default TextField;