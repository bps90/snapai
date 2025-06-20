"use client";
import Link from "next/link"
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

type MenuItem = {
    href: string,
    label: string,
    icon: string
}

const menuItems: MenuItem[] = [
    { href: '/dashboard/configuration', label: 'Configuration', icon: '⚙️' },
    { href: '/dashboard/controls', label: 'Controls', icon: '🎮' },
]

type MenuItemProps = {
    item: MenuItem;
    currentPathname: string;
}

function MenuItem({ item, currentPathname }: MenuItemProps) {
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

    return (<>
        <div className="aside-spacer min-w-60"></div>
        <aside className="bg-gray-100 min-w-60 py-4 fixed h-dvh flex items-center">
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