import { FormControl, FormControlProps, IconButton, InputAdornment, TextField, TextFieldProps, Tooltip } from "@mui/material";
import { FormFieldProps } from "./FormField";
import { Field } from '@/lib/fetchers';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export type NumberField = Field & {
    type: 'number',
    is_float: boolean,
    value: number,
    min_value: number | null,
    max_value: number | null
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
    inputAttr,
    nestedPaths
}: NumberFieldProps) {
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
                type={field.type}
                slotProps={{
                    htmlInput: {
                        step: field.is_float ? 'any' : '1',
                        min: field.min_value,
                        max: field.max_value
                    },
                    input: {
                        endAdornment: (
                            field.informative?.help_text && (
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

                        )
                    }
                }}
                id={field.id}
                required={field.required}
                {...register(nameAsArray.join('.'), { valueAsNumber: true, onChange: (e) => field.afterChange?.(Number(e.target.value)) })}
                {...inputAttr}
            />
        </FormControl>
    </div>);
}