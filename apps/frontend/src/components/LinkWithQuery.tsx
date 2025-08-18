"use client";

import Link, { LinkProps } from "next/link";
import { useSearchParams } from "next/navigation";
import { AnchorHTMLAttributes } from "react";

export type LinkWithQueryProps = Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof LinkProps> & LinkProps & { children: React.ReactNode };

export default function LinkWithQuery({ href, ...props }: LinkWithQueryProps) {
    const searchParams = useSearchParams();
    const query = searchParams.toString();
    const finalHref = typeof href === "string" ? `${href}${query ? `?${query}` : ""}` : href;

    return <Link href={finalHref} {...props} />;
}