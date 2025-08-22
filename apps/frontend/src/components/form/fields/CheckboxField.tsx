import { Field } from "@/lib/fetchers";
import { FormFieldProps } from "./FormField";
import { Checkbox, CheckboxProps, FormControl, FormControlLabel, FormControlLabelProps, FormControlProps, FormHelperText, IconButton, Tooltip } from "@mui/material";
import clsx from "clsx";
import { Controller, useFormState } from "react-hook-form";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { useState } from "react";

export type CheckboxField = Field & {
    type: 'checkbox',
    value: boolean,
}

export type CheckboxFieldProps = FormFieldProps & {
    field: CheckboxField,
    checkboxAttr?: CheckboxProps,
    formControlAttr?: FormControlProps,
    formControlLabelAttr?: FormControlLabelProps,
}

export default function CheckboxField({
    field,
    fieldIndex,
    containerAttr,
    checkboxAttr,
    formControlAttr,
    formControlLabelAttr,
    nestedPaths,
    control
}: CheckboxFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];
    const error = control.getFieldState(nameAsArray.join('.'))?.error?.message;

    return (
        <div
            key={field.id + fieldIndex}
            style={{ gridColumn: `span ${field.occuped_columns}` }}
            {...containerAttr}
        >
            <FormControl
                sx={{
                    px: 1.5,
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    flexDirection: 'row',
                    height: '100%',
                    minHeight: '56px',
                }}
                variant="outlined"
                fullWidth
                {...formControlAttr}
                className={clsx(
                    'h-full',
                    formControlAttr?.className
                )}
            >
                <Controller
                    name={nameAsArray.join('.')}
                    control={control}
                    render={({ field: controllerField, fieldState: { error } }) => {
                        return (
                            <FormControlLabel
                                title={field.informative?.title}
                                control={
                                    <Checkbox
                                        required={field.required}
                                        id={field.id}
                                        checked={controllerField.value ?? false}
                                        onChange={(e) => {
                                            controllerField.onChange(e.target.checked);
                                            field.afterChange?.(e.target.checked);
                                        }}
                                        {...checkboxAttr}
                                    />
                                }
                                label={<>{field.label}{field.required && <span className="opacity-60">*</span>}</>}
                                {...formControlLabelAttr}
                            />
                        )
                    }}
                />
                {field.informative?.help_text &&
                    <Tooltip
                        arrow
                        placement="bottom-end"
                        title={field.informative.as_html
                            ? <span dangerouslySetInnerHTML={{ __html: field.informative.help_text }}></span>
                            : field.informative.help_text}>
                        <IconButton disableTouchRipple sx={{ mr: '-8px' }}>
                            <HelpOutlineIcon fontSize="small" />
                        </IconButton>
                    </Tooltip>}
            </FormControl>
            {error && <FormHelperText error>{error}</FormHelperText>}
        </div>
    )
}