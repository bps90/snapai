"use client";
import { SimulationContextProps, useSimulationContext } from "@/contexts/SimulationContext";
import { Tooltip } from "@mui/material";
import Link from "next/link"
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

type MenuItem = {
    href: string,
    label: string,
    icon: string,
    enabler?: (simulationContext: SimulationContextProps, currentPathname: string) => boolean,
}

const menuItems: MenuItem[] = [
    { href: '/dashboard/configuration', label: 'Configuration', icon: '⚙️' },
    {
        href: '/dashboard/controls',
        label: 'Controls',
        icon: '🎮',
        enabler: (simulationContext, currentPathname) => {
            return !!simulationContext.selectedProject
        }
    },
]

type MenuItemProps = {
    item: MenuItem;
    currentPathname: string;
}

function MenuItem({ item, currentPathname }: MenuItemProps) {
    const simulationContext = useSimulationContext();
    const [isActive, setIsActive] = useState(false);
    const [isEnabled, setIsEnabled] = useState(false);

    const verifyActive = () => {
        setIsActive(item.href === currentPathname)
    };

    useEffect(verifyActive, [item.href, currentPathname])
    useEffect(() => {
        if (item.enabler) {
            setIsEnabled(item.enabler(simulationContext, currentPathname));
        } else {
            setIsEnabled(true);
        }
    })

    return (
        <Link
            href={isEnabled ? item.href : "#"}
            style={{
                cursor: isEnabled ? "pointer" : "not-allowed",
                opacity: isEnabled ? 1 : 0.5
            }}
            className={"px-4 py-2 block" + (isActive ? " bg-blue-600 text-white" : "")}
        >
            <span>{item.icon}</span>
            <span className="aside-item-label ml-4">{item.label}</span>
        </Link>
    )
}

export default function SideMenu() {
    const pathname = usePathname();

    return (<>
        <div className="aside-spacer min-w-13 simulation-aside-"></div>
        <aside className="overflow-y-auto text-nowrap overflow-x-clip bg-gray-100 py-4 fixed h-dvh flex items-center simulation-aside z-10">
            <ul className="flex flex-col gap-2 w-full">
                {menuItems.map((item) => (
                    <li key={item.href}>
                        <MenuItem item={item} currentPathname={pathname} />
                    </li>
                ))}
            </ul>
        </aside>
    </>)
}