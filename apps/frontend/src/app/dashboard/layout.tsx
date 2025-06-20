import SideMenu from "@/components/SideMenu";
import { SimulationProvider } from "@/contexts/SimulationContext";

type DashBoardLayoutProps = {
    children: React.ReactNode;
};

export default function DashboardLayout({
    children,
}: DashBoardLayoutProps) {
    return <SimulationProvider>
        <div className="flex">
            <SideMenu />
            {children}
        </div>
    </SimulationProvider>;
}