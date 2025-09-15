import { FormControl, FormControlProps, IconButton, InputAdornment, TextField, TextFieldProps, Tooltip } from "@mui/material";
import { FormFieldProps } from "./FormField";
import { Field } from '@/lib/fetchers';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { Controller } from "react-hook-form";
import clsx from "clsx";
import { useState } from "react";
import AngleDropdown from "@/components/AngleDropdown";

export type NumberField = Field & {
    type: 'number',
    is_float: boolean,
    value: number,
    min_value: number | null,
    is_angle: false | 'rad' | 'deg',
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
    containerAttr,
    formControlAttr,
    inputAttr,
    control,
    nestedPaths
}: NumberFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];
    const [focused, setFocused] = useState<boolean>(false);

    return (<div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
        className={clsx('relative', containerAttr?.className)}
    >

        <Controller
            name={nameAsArray.join('.')}
            control={control}
            rules={{ required: field.required }}
            defaultValue={field.value ?? 0}
            render={({ field: controllerField, fieldState: { error } }) => (<>
                <FormControl fullWidth {...formControlAttr}>
                    <TextField
                        variant='outlined'
                        label={field.label}
                        type={field.type}
                        helperText={error?.message}
                        onChange={(e) => {
                            controllerField.onChange(Number(e.target.value));
                            field.afterChange?.(Number(e.target.value));
                        }}
                        onFocus={() => setFocused(true)}
                        onBlur={() => setFocused(false)}
                        value={controllerField.value}
                        slotProps={{
                            htmlInput: {
                                step: 'any',
                                min: field.min_value,
                                max: field.max_value
                            },
                            formHelperText: {
                                error: true,
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
                        {...inputAttr}
                    />
                </FormControl>
                {field.is_angle && focused && <AngleDropdown
                    angle={controllerField.value}
                    isDegrees={field.is_angle === 'deg'}
                    is_float={field.is_float}
                    max_value={field.max_value}
                    min_value={field.min_value}
                    onChange={(angle) => {
                        controllerField.onChange(angle);
                        field.afterChange?.(angle);
                    }}
                    onFocusAdjusments={() => setFocused(true)}
                    onBlurAdjusments={() => setFocused(false)}
                />
                }
            </>)
            }
        >

        </Controller>


    </div >);
}