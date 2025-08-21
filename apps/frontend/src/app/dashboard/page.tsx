import LinkWithQuery from "@/components/LinkWithQuery";
import { Button } from "@mui/material";

export default function Dashboard() {
    return (
        <main className="flex flex-col w-full items-center justify-center min-h-screen px-4 col-start-3 col-end-13">
            <h1 className="text-5xl font-bold text-gray-900 mb-8 text-center">
                Start working with <span className="text-blue-600">SnapAI</span>
            </h1>

            <LinkWithQuery
                href="/dashboard/configuration"
                className="text-lg font-semibold"
            >
                <Button
                    style={{
                        padding: "1rem 2rem",
                        font: 'inherit',
                        fontFamily: "'Geist Mono', sans-serif",
                        borderRadius: '1rem',
                    }}
                    variant="contained"
                    size="large" >Start by configuring your project ⚙️</Button>
            </LinkWithQuery>
        </main>

    );
}