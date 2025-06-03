import SideMenu from "@/components/SideMenu";
import { SimulationProvider } from "@/contexts/SimulationContext";

interface IDashBoardLayoutProps {
    children: React.ReactNode;
};

export default function DashboardLayout({
    children,
}: IDashBoardLayoutProps) {
    return <SimulationProvider>
        <div className="grid grid-cols-12 h-lvh">
            <SideMenu />
            {children}
        </div>
    </SimulationProvider>;
}