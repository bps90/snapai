import { Chip, ChipProps, IconButton, IconButtonProps } from "@mui/material"
import Image from "next/image"
import { ReactElement } from "react"

export type ControlButtonProps<Label extends string | undefined> = (Label extends string ? ChipProps : IconButtonProps) & {
    icon?: ReactElement,
    iconImage?: {
        src: string,
        alt: string
    }
    label?: Label,
}

export default function ControlButton<Label extends string | undefined>({
    icon,
    iconImage,
    label,
    ...props
}: ControlButtonProps<Label>) {
    return label ? (
        <Chip
            icon={icon ?? (iconImage && <Image
                src={iconImage.src}
                alt={iconImage.alt}
                width={20}
                height={20}
            />)}
            label={<span className="font-bold">{label}</span>}
            variant="outlined"
            clickable
            {...(props as ChipProps)}
        />
    ) : (
        <IconButton
            sx={{
                border: "1px solid #ccc",
                padding: "4px",
            }}
            className="rounded-full w-8 h-8"
            {...(props as IconButtonProps)}
        >
            {icon ?? (iconImage && <Image
                src={iconImage.src}
                alt={iconImage.alt}
                width={20}
                height={20}
            />)}
        </IconButton>
    );
}