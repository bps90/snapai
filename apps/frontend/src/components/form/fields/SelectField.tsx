import { Field } from "@/lib/fetchers"
import { FormFieldProps } from "./FormField"
import { FormControl, FormControlProps, IconButton, InputAdornment, InputLabel, MenuItem, Select, SelectProps, Tooltip } from "@mui/material"
import { Controller } from "react-hook-form"
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

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
                            endAdornment={
                                field.informative?.help_text && (
                                    <InputAdornment position="end">
                                        <Tooltip
                                            arrow
                                            placement="bottom-end"
                                            title={field.informative.as_html
                                                ? <span dangerouslySetInnerHTML={{ __html: field.informative.help_text }}></span>
                                                : field.informative.help_text}>
                                            <IconButton disableTouchRipple sx={{ mr: '16px' }}>
                                                <HelpOutlineIcon fontSize="small" />
                                            </IconButton>
                                        </Tooltip>
                                    </InputAdornment>
                                )
                            }
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