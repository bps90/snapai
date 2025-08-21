import { Field } from '@/lib/fetchers';
import { FormControl, FormControlProps, IconButton, InputAdornment, TextField as MaterialTextField, TextFieldProps as MaterialTextFieldProps, TextField as ColorField, Tooltip } from '@mui/material';
import { FormFieldProps } from './FormField';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export type ColorField = Field & {
    type: 'color'
    value: `#${string}`,
}

export type ColorFieldProps = FormFieldProps & {
    inputAttr?: MaterialTextFieldProps,
    formControlAttr?: FormControlProps,
    field: ColorField,
}


function ColorField({
    field,
    fieldIndex,
    inputAttr,
    containerAttr,
    formControlAttr,
    nestedPaths,
    register
}: ColorFieldProps) {
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
                {...register(nameAsArray.join('.'), {
                    onChange: (e) => field.afterChange?.(e.target.value),
                })}
                {...inputAttr}
            />
        </FormControl>
    </div>;
}

export default ColorField;