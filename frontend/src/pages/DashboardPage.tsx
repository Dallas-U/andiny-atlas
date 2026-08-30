import { useState } from "react";

import DashboardHeader from "../features/dashboard/components/DashboardHeader";
import WelcomeCard from "../features/dashboard/components/WelcomeCard";
import QuickActions from "../features/dashboard/components/QuickActions";
import InvestigationStatistics from "../features/dashboard/components/InvestigationStatistics";
import RecentInvestigations from "../features/dashboard/components/RecentInvestigations";
import SystemStatus from "../features/dashboard/components/SystemStatus";

import EnterpriseKpiCards from "../features/enterprise-dashboard/components/EnterpriseKpiCards";
import BranchPerformancePanel from "../features/enterprise-dashboard/components/BranchPerformancePanel";
import DepartmentPerformancePanel from "../features/enterprise-dashboard/components/DepartmentPerformancePanel";
import ExecutiveSummaryPanel from "../features/enterprise-dashboard/components/ExecutiveSummaryPanel";

import { useAuth } from "../shared/auth/AuthContext";

function DashboardPage() {
    const {
        currentUser,
    } = useAuth();

    const [
        selectedBranchId,
        setSelectedBranchId,
    ] = useState<string | null>(null);

    const organizationId =
        currentUser?.organization_id;

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <DashboardHeader />

            <WelcomeCard />

            <EnterpriseKpiCards />

            <ExecutiveSummaryPanel />

            {organizationId ? (
                <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                    <BranchPerformancePanel
                        organizationId={
                            organizationId
                        }
                        selectedBranchId={
                            selectedBranchId
                        }
                        onSelectBranch={
                            setSelectedBranchId
                        }
                    />

                    <DepartmentPerformancePanel
                        selectedBranchId={
                            selectedBranchId
                        }
                    />
                </div>
            ) : (
                <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                    <h2 className="text-lg font-semibold text-white">
                        Enterprise Structure
                    </h2>

                    <p className="mt-2 text-sm text-slate-400">
                        Organization information is not
                        available for the current user.
                    </p>
                </section>
            )}

            <QuickActions />

            <InvestigationStatistics />

            <RecentInvestigations />

            <SystemStatus />
        </main>
    );
}

export default DashboardPage;