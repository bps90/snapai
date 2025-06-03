import Link from "next/link";

export default function Dashboard() {
    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4 col-start-3 col-end-13">
            <h1 className="text-5xl font-bold text-gray-900 mb-8 text-center">
                Start work with <span className="text-blue-600">SnapAI</span>
            </h1>

            <Link
                href="/dashboard/configuration"
                className="inline-flex items-center px-8 py-4 text-lg font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-2xl shadow-lg transition duration-300"
            >
                Start by configuring your project ⚙️
            </Link>
        </main>

    );
}