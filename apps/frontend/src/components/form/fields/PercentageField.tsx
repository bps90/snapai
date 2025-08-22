import { FormControl, FormControlProps, IconButton, InputAdornment, TextField, TextFieldProps, Tooltip } from "@mui/material";
import { FormFieldProps } from "./FormField";
import { NumberField } from "./NumberField";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

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
    control,
    nestedPaths
}: PercentageFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];
    const error = control.getFieldState(nameAsArray.join('.'))?.error?.message;

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
                    formHelperText: { error: true },
                    htmlInput: { step: field.is_float ? 'any' : '1', min: field.min_value, max: field.max_value },
                    input: {
                        endAdornment: (<>
                            <InputAdornment position="end">%</InputAdornment>
                            {field.informative?.help_text && (
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
                            )}
                        </>)
                    }
                }}
                helperText={error}
                id={field.id}
                required={field.required}
                {...register(nameAsArray.join('.'), { valueAsNumber: true, onChange: (e) => field.afterChange?.(Number(e.target.value)) })}
                {...inputAttr}
            />
        </FormControl>
    </div>);
}