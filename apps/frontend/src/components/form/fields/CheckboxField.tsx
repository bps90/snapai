import { Field } from "@/lib/fetchers";
import { FormFieldProps } from "./FormField";
import { Checkbox, CheckboxProps, FormControl, FormControlLabel, FormControlLabelProps, FormControlProps } from "@mui/material";
import clsx from "clsx";
import { Controller } from "react-hook-form";

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
                    justifyContent: 'center',
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
                    render={({ field: controllerField }) => (
                        <FormControlLabel
                            control={
                                <Checkbox
                                    required={field.required}
                                    id={field.id}
                                    checked={controllerField.value ?? false}
                                    onChange={(e) => controllerField.onChange(e.target.checked)}
                                    {...checkboxAttr}
                                />
                            }
                            label={field.label}
                            {...formControlLabelAttr}
                        />
                    )}
                />
            </FormControl>
        </div>
    )
}