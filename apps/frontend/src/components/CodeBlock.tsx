import { Box, } from '@mui/material';
import clsx from 'clsx';

export type CodeBlockProps = {
    code: string | React.ReactNode,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    boxAttr?: any;
}

export default function CodeBlock({ code, boxAttr }: CodeBlockProps) {
    return (
        <Box
            component="pre"
            {...boxAttr}
            className={clsx('rounded-lg', 'p-4', 'font-mono', 'text-sm', boxAttr?.className)}
        >
            <code>{code}</code>
        </Box>
    );
}