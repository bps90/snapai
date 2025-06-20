import { Field } from "@/lib/fetchers";
import { FormFieldProps } from "./FormField";
import { Controller, ControllerProps } from "react-hook-form";
import { ConfigFormSchema } from "../ConfigForm";
import { Box, Divider, InputLabel, TextField } from "@mui/material";
import clsx from "clsx";

export type NumberPairField = Field & {
    type: 'number_pair',
    value: [number, number],
    is_float: boolean,
}

export type NumberPairFieldProps = FormFieldProps & {
    field: NumberPairField,
    controllerAttr?: ControllerProps,
};

export default function NumberPairField({
    control,
    field,
    fieldIndex,
    containerAttr,
}: NumberPairFieldProps) {
    return <div
        key={field.id + fieldIndex}
        style={{ gridColumn: `span ${field.occuped_columns}` }}
        {...containerAttr}
    >
        <Controller
            control={control}
            name={field.name as keyof ConfigFormSchema}
            defaultValue={field.value}

            render={({ field: renderField, fieldState }) => {
                const [min, max] = renderField.value as [number, number];
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
                        display="flex"
                        alignItems="center"
                        sx={{
                            display: 'flex',
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
                            onChange={(e) => setMin(Number(e.target.value))}
                            error={!!fieldState.error}
                        />
                        <Divider orientation="vertical" flexItem />
                        <TextField
                            type="number"
                            value={max}
                            sx={{
                                '& fieldset': { border: 'none' },
                                flex: 1,
                            }}
                            onChange={(e) => setMax(Number(e.target.value))}
                            error={!!fieldState.error}
                            helperText={fieldState.error?.message}
                        />
                    </Box></>
                );
            }}
        />
    </div>;
}