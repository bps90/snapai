import { Chip, ChipProps, IconButton, IconButtonProps, Tooltip } from "@mui/material"
import Image from "next/image"
import { ReactElement, ReactNode } from "react"

export type ControlButtonProps<Label extends string | undefined> = (Label extends string ? ChipProps : IconButtonProps) & {
    icon?: ReactElement,
    iconImage?: {
        src: string,
        alt: string
    }
    label?: Label,
    helpText?: ReactNode,
}

export default function ControlButton<Label extends string | undefined>({
    icon,
    iconImage,
    label,
    helpText,
    ...props
}: ControlButtonProps<Label>) {
    return <Tooltip
        arrow
        title={helpText}
    >
        <div>
            {label ? (
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
                    {...(props as IconButtonProps)}
                    sx={{
                        border: "1px solid #ccc",
                        padding: "4px",
                        ...(props as IconButtonProps).sx
                    }}
                    className={`rounded-full w-8 h-8 ${(props as IconButtonProps).className}`}

                >
                    {icon ?? (iconImage && <Image
                        src={iconImage.src}
                        alt={iconImage.alt}
                        width={20}
                        height={20}
                    />)}
                </IconButton>
            )}
        </div>
    </Tooltip>;
}