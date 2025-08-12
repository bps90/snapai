import { Field } from "@/lib/fetchers";
import { FormFieldProps } from "./FormField";
import { Controller, ControllerProps } from "react-hook-form";
import { Box, Divider, FormHelperText, IconButton, InputAdornment, InputLabel, TextField, TextFieldProps, Tooltip } from "@mui/material";
import clsx from "clsx";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export type NumberPairField = Field & {
    type: 'number_pair',
    value: [number, number],
    is_float: boolean,
    min_left_value: number | null,
    max_left_value: number | null,
    min_right_value: number | null,
    max_right_value: number | null,
    right_should_be_gte_left: boolean
}

export type NumberPairFieldProps = FormFieldProps & {
    field: NumberPairField,
    controllerAttr?: ControllerProps,
    inputsAttr?: TextFieldProps,
};

export default function NumberPairField({
    control,
    field,
    fieldIndex,
    containerAttr,
    inputsAttr,
    nestedPaths
}: NumberPairFieldProps) {
    const nameAsArray = [...(nestedPaths ?? []), ...field.nested_paths, field.name];
    let leftGreaterThanRight: NodeJS.Timeout | null = null;

    return <div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
    >
        <Controller
            control={control}
            name={nameAsArray.join('.')}
            defaultValue={field.value}

            render={({ field: renderField, fieldState }) => {
                const [min, max] = renderField.value ?? [0, 0] as [number, number];
                const setMin = (val: number) => renderField.onChange([val, max]);
                const setMax = (val: number) => renderField.onChange([min, val]);
                return (<>
                    <InputLabel
                        shrink
                        id={`input_label_${field.id}_index_${fieldIndex}`}
                        className={clsx(
                            "ml-2",
                            "block",
                            "pl-2",
                            "-mb-4",
                            "bg-white",
                            "w-min"
                        )}
                        style={{
                            padding: '0 8px',
                        }}
                    >
                        {field.label}
                    </InputLabel>
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            border: '1px solid rgba(0, 0, 0, 0.23)',
                            borderRadius: '4px',
                        }}>
                        <TextField
                            type="number"
                            value={min}
                            sx={{
                                '& fieldset': { border: 'none' },
                                flex: 1,
                            }}
                            slotProps={{ htmlInput: { min: field.min_left_value, max: field.max_left_value } }}
                            onChange={(e) => setMin(Number(e.target.value))}
                            error={!!fieldState.error}
                            {...inputsAttr}
                        />
                        <Divider orientation="vertical" flexItem />
                        <TextField
                            type="number"
                            value={max}
                            sx={{
                                '& fieldset': { border: 'none' },
                                flex: 1,
                            }}
                            slotProps={{
                                htmlInput: {
                                    min: field.min_right_value,
                                    max: field.max_right_value
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
                            onChange={(e) => setMax(Number(e.target.value))}
                            error={!!fieldState.error}
                            {...inputsAttr}
                        />
                    </Box>
                    {fieldState.error?.message && (
                        <FormHelperText className="block w-full" error>
                            {fieldState.error.message}
                        </FormHelperText>
                    )}
                </>
                );
            }}
        />
    </div>;
}