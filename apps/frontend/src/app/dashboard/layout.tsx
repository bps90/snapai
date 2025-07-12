import SideMenu from "@/components/SideMenu";
import { SimulationProvider } from "@/contexts/SimulationContext";
import { ErrorModalProvider } from '@/contexts/ErrorModalContext';

type DashBoardLayoutProps = {
    children: React.ReactNode;
};

export default function DashboardLayout({
    children,
}: DashBoardLayoutProps) {
    return <ErrorModalProvider>
        <SimulationProvider>
            <div className="flex">
                <SideMenu />
                {children}
            </div>
        </SimulationProvider>
    </ErrorModalProvider>;
}