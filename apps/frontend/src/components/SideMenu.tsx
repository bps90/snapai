"use client";
import Link from "next/link"
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

interface IMenuItem {
    href: string,
    label: string,
    icon: string
}

const menuItems: IMenuItem[] = [
    { href: '/dashboard/configuration', label: 'Configuration', icon: '⚙️' },
    { href: '/dashboard/controls', label: 'Controls', icon: '🎮' },
]

interface IMenuItemProps {
    item: IMenuItem;
    currentPathname: string;
}

function MenuItem({ item, currentPathname }: IMenuItemProps) {
    const [isActive, setIsActive] = useState(false);

    const verifyActive = () => {
        setIsActive(item.href === currentPathname)
    };

    useEffect(verifyActive, [item.href, currentPathname])

    return (
        <Link href={item.href} className={"px-4 py-2 block" + (isActive ? " bg-blue-600 text-white" : "")}>
            <span>{item.icon}</span> <span>{item.label}</span>
        </Link>
    )
}

export default function SideMenu() {
    const pathname = usePathname();

    return (
        <aside className="bg-gray-100 col-span-2 py-8">
            <ul className="flex flex-col gap-2">
                {menuItems.map((item) => (
                    <li key={item.href}>
                        <MenuItem item={item} currentPathname={pathname} />
                    </li>
                ))}
            </ul>
        </aside>
    )
}