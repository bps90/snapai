import { Tooltip } from "@mui/material";
import clsx from "clsx";
import Image from "next/image";
import { HTMLAttributes, ReactElement, ReactNode } from "react";

export type SimulationInfoChipProps = {
    icon?: ReactElement;
    iconImage?: {
        src: string;
        alt: string;
    }
    text: string;
    title: ReactNode;
    fullWidth?: boolean;
    boxAttr?: HTMLAttributes<HTMLDivElement>;
}

export default function SimulationInfoChip({
    icon, iconImage, text, fullWidth, title, boxAttr
}: SimulationInfoChipProps) {
    return (
        <Tooltip
            arrow
            title={title}
        >
            <div
                {...boxAttr}
                className={clsx('flex',
                    fullWidth && 'w-full',
                    'items-center',
                    'justify-between',
                    'gap-2',
                    'bg-gray-100',
                    'h-15',
                    'py-4',
                    'px-2',
                    'rounded-md',
                    'shadow-md',
                    boxAttr?.className,
                )}>
                {icon ?? (iconImage && <Image
                    src={iconImage.src}
                    alt={iconImage.alt}
                    width={35}
                    height={35}
                />)}
                <p className="block font-bold text-gray-700 font-mono">
                    {text}
                </p>
            </div>
        </Tooltip>
    )
}