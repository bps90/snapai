import { Field } from "@/lib/fetchers";
import { FormFieldProps } from "./FormField";
import { Checkbox, CheckboxProps, FormControl, FormControlLabel, FormControlLabelProps, FormControlProps } from "@mui/material";
import clsx from "clsx";

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
    register,
    containerAttr,
    checkboxAttr,
    formControlAttr,
    formControlLabelAttr,
    nestedPaths
}: CheckboxFieldProps) {
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
                }}
                variant="outlined"
                fullWidth
                {...formControlAttr}
                className={clsx(
                    'h-full',
                    formControlAttr?.className
                )}
            >
                <FormControlLabel
                    control={
                        <Checkbox
                            id={field.id}
                            checked={field.value}
                            {...register(`${nestedPaths?.length ? nestedPaths.join('.') + '.' : ''}${field.nested_paths.length ? (field.nested_paths.join('.') + '.') : ''}${field.name}`)}
                            {...checkboxAttr}
                        />
                    }
                    label={field.label}
                    {...formControlLabelAttr}
                />
            </FormControl>
        </div>
    )
}