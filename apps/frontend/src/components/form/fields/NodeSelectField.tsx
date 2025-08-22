import { FormFieldProps } from "./FormField"
import { FormControl, FormControlProps, FormHelperText, IconButton, InputAdornment, InputLabel, MenuItem, Select, SelectProps, Tooltip } from "@mui/material"
import { SelectField } from "./SelectField"
import { Controller } from "react-hook-form"
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export type NodeSelectField = Omit<SelectField, 'type' | 'value' | 'options'> & {
    type: 'node_select',
    value: string,
    options: ({ value: string, label: string })[]
}

export type NodeSelectFieldProps = FormFieldProps & {
    field: NodeSelectField,
    formControlAttr?: FormControlProps,
    selectAttr?: SelectProps,
    onNodeNameChange?: (nodeName: string) => void
}

export default function NodeSelectField({
    nestedPaths,
    field,
    control,
    selectAttr,
    formControlAttr,
    fieldIndex,
    containerAttr,
    onNodeNameChange,
}: NodeSelectFieldProps) {
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
                    render={({ field: controllerField, fieldState }) => (<>
                        <Select
                            labelId={name + '__label'}
                            variant="outlined"
                            label={field.label}
                            id={field.id}
                            {...controllerField}
                            {...selectAttr}
                            onChange={(e, child) => {
                                controllerField.onChange(e, child);
                                selectAttr?.onChange?.(e, child);
                                onNodeNameChange?.(nameAsArray.join('.'));
                                field.afterChange?.(e.target.value);
                            }}
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
                        {fieldState.error && <FormHelperText error>{fieldState.error.message}</FormHelperText>}
                    </>)}
                />
            </FormControl>
        </div>
    );
}