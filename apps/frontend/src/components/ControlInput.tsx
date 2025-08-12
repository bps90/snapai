import { IconButton, InputAdornment, TextField, Tooltip } from "@mui/material"
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { HTMLInputTypeAttribute, ReactNode } from "react";
import { UseFormRegisterReturn } from "react-hook-form";

export type ControlInputProps = {
    placeholder?: string
    title?: string
    helpText?: ReactNode
    type: HTMLInputTypeAttribute
    register: UseFormRegisterReturn
    min?: number
    max?: number
    minLength?: number
    maxLength?: number
    error?: string
}

export default function ControlInput({
    placeholder,
    title,
    helpText,
    register,
    min,
    max,
    minLength,
    maxLength,
    type,
    error
}: ControlInputProps) {
    return (
        <Tooltip
            title={title ?? placeholder}
            placement="top"
            arrow
        >
            <TextField
                hiddenLabel
                variant="outlined"
                size="small"
                type={type}
                error={!!error}
                helperText={error}
                placeholder={placeholder}
                slotProps={{
                    htmlInput: {
                        min,
                        max,
                        minLength,
                        maxLength
                    },
                    input: {
                        endAdornment: (
                            <InputAdornment position="end">
                                <Tooltip
                                    arrow
                                    title={helpText ?? title ?? placeholder}
                                >
                                    <IconButton edge="end" size="small" sx={{ mr: '-12px', ml: '-8px' }} disableTouchRipple>
                                        <HelpOutlineIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </InputAdornment>
                        )
                    }
                }}
                sx={{
                    width: '120px',
                    position: 'relative',
                    '& .MuiOutlinedInput-root': {
                        borderRadius: '50px',
                        height: '32px',
                        width: '120px',
                        fontSize: '12px',
                    },
                    '& .MuiFormHelperText-root': {
                        position: 'absolute',
                        width: '100%',
                        margin: 0,
                        left: 0,
                        top: 0 + 36,
                        borderRadius: '4px',
                        background: 'white', // opcional, para não misturar com fundo
                        padding: '0 4px',    // opcional
                    },
                }}
                {...register}
            />
        </Tooltip>
    )
}