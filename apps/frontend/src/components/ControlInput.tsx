import { IconButton, InputAdornment, TextField, Tooltip } from "@mui/material"
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { ReactNode } from "react";

export type ControlInputProps = {
    placeholder?: string
    title?: string
    helpText?: ReactNode
}

export default function ControlInput({
    placeholder,
    title,
    helpText
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
                type="number"
                placeholder={placeholder}
                slotProps={{
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
                    '& .MuiOutlinedInput-root': {
                        borderRadius: '50px',
                        height: '32px',
                        width: '120px',
                        fontSize: '12px',
                    },
                }}
            />
        </Tooltip>
    )
}