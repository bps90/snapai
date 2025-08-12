import { Field } from '@/lib/fetchers';
import { FormControl, FormControlProps, IconButton, InputAdornment, TextField as MaterialTextField, TextFieldProps as MaterialTextFieldProps, TextField, Tooltip } from '@mui/material';
import { FormFieldProps } from './FormField';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export type TextField = Field & {
    type: 'text'
    value: string,
    min_length: number,
    max_length: number | null
}

export type TextFieldProps = FormFieldProps & {
    inputAttr?: MaterialTextFieldProps,
    formControlAttr?: FormControlProps,
    field: TextField,
}

function TextField({
    field,
    fieldIndex,
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
                slotProps={{
                    htmlInput: {
                        minLength: field.min_length,
                        maxLength: field.max_length
                    },
                    input: {
                        endAdornment: field.informative?.help_text && (
                            <InputAdornment position="end">
                                <Tooltip
                                    arrow
                                    placement="bottom-end"
                                    title={field.informative.as_html
                                        ? <span dangerouslySetInnerHTML={{ __html: field.informative.help_text }}></span>
                                        : field.informative.help_text}>
                                    <IconButton disableTouchRipple sx={{ mr: '-8px' }}>
                                        <HelpOutlineIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </InputAdornment>
                        )
                    }
                }}
                {...register(nameAsArray.join('.'))}
                {...inputAttr}
            />
        </FormControl>
    </div>;
}

export default TextField;